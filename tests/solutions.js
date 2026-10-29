async page => {
  const labs=await page.evaluate(()=>JSON.parse(document.getElementById('lab-data').textContent).filter(l=>l.lang==='r'));
  const results=[];
  for(const lab of labs) {
    await page.locator('#lab-'+lab.id+'-code').fill(lab.solution);
    await page.locator('#lab-'+lab.id+' .primary').click();
    await page.waitForFunction(id=>!document.querySelector('#lab-'+id+' .primary').disabled,lab.id,{timeout:45000});
    const result=await page.locator('#lab-'+lab.id+' .lab-status').textContent();
    results.push({id:lab.id,status:result,plots:await page.locator('#lab-'+lab.id+' canvas').count()});
  }
  return results;
}

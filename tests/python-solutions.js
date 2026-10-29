async page => {
  const labs=await page.evaluate(()=>JSON.parse(document.getElementById('lab-data').textContent).filter(l=>l.lang==='python'));
  const results=[];
  for(const lab of labs) {
    await page.locator('#lab-'+lab.id+'-code').fill(lab.solution);
    await page.locator('#lab-'+lab.id+' .primary').click();
    await page.waitForFunction(id=>!document.querySelector('#lab-'+id+' .primary').disabled,lab.id,{timeout:45000});
    results.push({id:lab.id,status:await page.locator('#lab-'+lab.id+' .lab-status').textContent(),output:(await page.locator('#lab-'+lab.id+' .lab-output').textContent()).slice(0,150)});
  }
  return results;
}

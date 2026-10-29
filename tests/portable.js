async page => {
  const base=new URL(page.url()).origin;
  const imported={id:'py-limit',code:'def max_n(limit):\n    return 0\n# imported',stdin:''};
  await page.goto(base+'/?import-test=1#practice='+encodeURIComponent(JSON.stringify(imported)));
  if(await page.locator('#lab-py-limit-code').inputValue()!==imported.code)throw new Error('Imported code was lost');
  if((await page.locator('#lab-py-limit .lab-status').textContent()).includes('실행 중'))throw new Error('Imported code auto-executed');
  await page.locator('#lab-py-limit .primary').click();
  await page.waitForFunction(()=>!document.querySelector('#lab-py-limit .primary').disabled,null,{timeout:45000});
  if((await page.locator('#lab-py-limit .lab-status').textContent()).includes('완료!'))throw new Error('Wrong imported code passed');
  await page.goto(base+'/?import-test=2#practice=bad-json');
  if(await page.locator('.lab').count()!==26)throw new Error('Malformed import broke page');
  return 'PASS: import preserves code, requires explicit execution, rejects incorrect solution, and ignores malformed links';
}

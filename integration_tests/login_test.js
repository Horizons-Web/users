Feature('Login');

Scenario('Successful login', ({ I }) => {
  I.amOnPage('https://frontend-3bsgyuggyq-ue.a.run.app/login');
  I.see('Sign in to your account');
  I.fillField('Username', 'joaquinreyero');
  I.fillField('Password', 'rootroot');
  I.click('Login');
  I.waitForText('Adventures', 10);
  I.seeInCurrentUrl('https://frontend-3bsgyuggyq-ue.a.run.app/home');
});

Scenario('Fail login', ({ I }) => {
  I.amOnPage('https://frontend-3bsgyuggyq-ue.a.run.app/login');
  I.see('Sign in to your account');
  I.fillField('Username', 'joaquinreyero');
  I.fillField('Password', 'rootroot1');
  I.click('Login');
  I.seeInCurrentUrl('https://frontend-3bsgyuggyq-ue.a.run.app/login');
});
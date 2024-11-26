Feature('Login');

Scenario('Successful login', ({ I }) => {
  I.amOnPage('https://frontend-4713090974.us-east1.run.app/login');
  I.see('Sign in to your account');
  I.fillField('Username', 'test_user_ok');
  I.fillField('Password', 'test_password');
  I.click('Login');
  I.waitForText('Adventures', 10);
  I.seeInCurrentUrl('https://frontend-4713090974.us-east1.run.app/home');
});

Scenario('Fail login', ({ I }) => {
  I.amOnPage('https://frontend-4713090974.us-east1.run.app/login');
  I.see('Sign in to your account');
  I.fillField('Username', 'test_user_fail');
  I.fillField('Password', 'test_password');
  I.click('Login');
  I.seeInCurrentUrl('https://frontend-4713090974.us-east1.run.app/login');
});
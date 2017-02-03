
# Bestoon

A simple Income and Expense system.

## How to run

To run Bestoon in development mode; Just use steps bellow:

1. Install `python2`, `pip`, `virtualenv` in your system.
2. Clone the project `https://github.com/jadijadi/bestoon`.
3. Make development environment ready using commands bellow;

  ```bash
  git clone https://github.com/jadijadi/bestoon && cd bestoon
  virtualenv -p python2 build  # Create virtualenv named build
  source build/bin/activate
  pip install -r requirements.txt
  mv  bestoon/settings.py.sample bestoon/settings.py
  python manage.py migrate  # Create database tables
  ```

4. Run `Bestoon` using `python manage.py runserver`
5. Go to [http://localhost:8000](http://localhost:8000) to see your Bestoon version.

## Run tests

To run tests in Bestoon simply use `python manage.py test`.

If you want more verbosity you can use `-v` option with `0, 1, 2, or 3.`; e.g. `python manage.py test -v2`

## More Clients

The project contains two different clients (command line and an ionic app for android/iOS) but all the 3rd party clients are more than welcomed. Add yours below.

- [Ruby Console Clients API bestoon](http://github.com/shayanzare007/ruby-bestoon-api)
- [Angular 2 Web Client](https://github.com/n1arash/ngBestoon)
- [Bestoon Bash Script](https://github.com/moeinroid/Bestoon-bash-script)
- [Bestoon Client for windows](https://github.com/BakhtiariMohammad/Bestoon-Client-for-windows)
- [Bestoon Multiplatform Gui](https://github.com/alireza6677/BestoonGui)
- [Telegram Bot Client](https://github.com/farbodgame/bestoon-telegram)
- [Bestoon Telegram Bot](https://github.com/AlirezaieS/BestoonBot)
- [Bestoon Telegram Bot Client](https://github.com/MojtabaMonfared/BestoonClient)
- [BestoonMsn, a native Android client for Bestoon](https://github.com/theOneWithMind/BestoonMsn)
- [Bestoon php client](https://github.com/iamalirezaj/bestoon-php-client)



## TODO
- [x] a restful login service. user will give user pass and will get her token
- [x] local storage for ionic app. will store token and will using it when calling anything
- [x] create and submit the APK!
- [ ] expand the error messages on the server side. client should understand that token was not valid and refer user to login page
- [ ] logging system

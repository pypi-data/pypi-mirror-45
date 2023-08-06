## Gravatar URL

> Get the URL to a Gravatar image from an email

## Screenshot

<img src="https://gitlab.com/yoginth/gravatarurl/raw/master/Screenshot.png" width="550">

## Install

```
$ pip install gravatarurl
```

## Usage

```python
import gravatarurl as avatar

avatar.get('yoginth@zoho.com') # avatar.get('email@example.com')
#=> https://secure.gravatar.com/avatar/ef5eb22b653730b5d7d7c32a73ff64e7?s=250

avatar.get('yoginth@zoho.com', 500) # avatar.get('email@example.com', size)
#=> https://secure.gravatar.com/avatar/ef5eb22b653730b5d7d7c32a73ff64e7?s=500
```

## Get Help

There are few ways to get help:

 1. Please [post questions on Stack Overflow](https://stackoverflow.com/questions/ask). You can open issues with questions, as long you add a link to your Stack Overflow question.

 2. For bug reports and feature requests, open issues.

 3. For direct and quick help, you can [email me](mailto://yoginth@zoho.com).

## How to contribute
Have an idea? Found a bug? See [how to contribute][contributing].

Thanks!

## License

[MIT][license]

[LICENSE]: https://yoginth.mit-license.org/
[contributing]: /CONTRIBUTING.md

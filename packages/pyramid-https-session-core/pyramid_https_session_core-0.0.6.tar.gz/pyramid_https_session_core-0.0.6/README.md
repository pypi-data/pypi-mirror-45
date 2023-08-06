# pyramid_https_session_core

core https session extensions for pyramid

`pyramid_https_session_core` allows you to boostrap on a https only session factory

This does not provide for the session factory, but contains a means to build and
register the session factories.

This is a support package for new https-only interfaces to be built upon.

A MUCH BETTER WAY would be to do this via request methods.

This package will likely EOL or evolve into a variant that uses request methods.

support for https awareness
===========================

default values are `true`.  They can be set to `false`

*	session_https.ensure_scheme = true
*	beaker_session_https.ensure_scheme = true

If `request.scheme` is not "https", then `session_https` will be `None`.

`request.scheme` can be supported for backend proxies via paste deploy's prefix middleware:

Add this to your environment.ini's [app:main]

	filter-with = proxy-prefix

Then add this section

	[filter:proxy-prefix]
	use = egg:PasteDeploy#prefix


Developers
==========

Build out a function `initialize_https_session_support` that registers a factory with this package.

A reference implementation is available in pyramid_https_session_redis (see link below)

Several utility methods are provided to standardize how different libraries can map similar configuration options

Your users should just invoke your `initialize_https_session_support` as part of their startup

	def initialize_https_session_support(config, settings):
		https_session_factory = Foo()
		register_https_session_factory(config, settings, https_session_factory)

Supports
========

This package provides infrastructure to:

* https://github.com/jvanasco/pyramid_subscribers_beaker_https_session
* https://github.com/jvanasco/pyramid_https_session_redis


PyPi
==========

This package is available on PyPi

* https://pypi.python.org/pypi/pyramid_https_session_core


License
=======

MIT

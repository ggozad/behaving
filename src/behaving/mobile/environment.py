from . import setup, teardown


def before_all(context):
	pass

def before_feature(context, feature):
	pass


def before_scenario(context, scenario):
	setup(context)



def after_feature(context, feature):
	pass


def after_scenario(context, scenario):
	teardown(context)


def after_all(context):
	pass

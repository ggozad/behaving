import os
import json
import subprocess

from behave import step
from subprocess import check_output


def get_running_android_emulators():
    return [
        e.split("\t")[0]
        for e in subprocess.check_output(["adb", "devices"]).split("\n")
        if e.startswith("emulator-")
    ]


def get_name_from_android_emulator_id(emulator_id):
    try:
        return subprocess.check_output(
            ["adb", "-s", emulator_id, "emu", "avd", "name"]
        ).split("\r")[0]
    except:
        assert False, u"Emulator not found"


def get_android_emulator_id_from_name(name):
    emulators = get_running_android_emulators()
    for emulator in emulators:
        if name in subprocess.check_output(
            ["adb", "-s", emulator, "emu", "avd", "name"]
        ):
            return emulator
    assert False, u"Emulator not found"


@step(u'the iOS app at "{app_path}"')
def given_an_ios_app(context, app_path):
    # If the simulator exists
    app_path = os.path.join(context.mobile_app_dir, app_path)
    assert os.path.isdir(app_path), u"iOS app not found"
    app_path = os.path.abspath(app_path)
    context.ios_app = app_path


@step(u'the android app at "{app_path}"')
def given_an_android_app(context, app_path):
    # If the simulator exists
    app_path = os.path.join(context.mobile_app_dir, app_path)
    assert os.path.isfile(app_path), u"Android app not found"
    app_path = os.path.abspath(app_path)
    context.android_app = app_path


@step(u'I set the iOS capabilities to "{caps}"')
def set_ios_capabilities(context, caps):
    context.ios_capabilities = json.loads(caps)


@step(u'I set the android capabilities to "{caps}"')
def set_android_capabilities(context, caps):
    context.android_capabilities = json.loads(caps)


@step(u"I launch the app")
def launch_app(context):
    context.browser.driver.launch_app()


@step(u"I close the app")
def close_app(context):
    context.browser.driver.close_app()


@step(u"I background the app")
def background_app(context):
    context.browser.driver.background_app(-1)


@step(u"I background the app for {timeout:d} seconds")
def background_app_with_timeout(context, timeout):
    context.browser.driver.background_app(timeout)


@step(u"I quit the simulator")
def quit_simulator(context):
    if context.browser.driver_name == "ios":
        subprocess.call(["xcrun", "simctl", "shutdown", context.browser.udid()])
    elif context.browser.driver_name == "android":
        subprocess.call(["adb", "emu", "kill"])

    name = context.persona["id"]
    del context.browsers[name]


@step(u'I add "{path}" to the photo library')
def add_media(context, path):
    path = os.path.join(context.attachment_dir, path)
    if context.browser.driver_name == "ios":
        subprocess.call(["xcrun", "simctl", "addmedia", context.browser.udid(), path])
    elif context.browser.driver_name == "android":
        name = context.persona["id"]
        emulator_id = get_android_emulator_id_from_name(name)
        check_output(["adb", "-s", emulator_id, "push", path, "/sdcard/Pictures"])
        check_output(
            [
                "adb",
                "-s",
                emulator_id,
                "shell",
                "am",
                "broadcast",
                "-a",
                "android.intent.action.MEDIA_MOUNTED",
                "-d",
                "file:///mnt/sdcard/Pictures",
            ]
        )


@step(u'I add vcard "{path}" to my contact list')
def add_contact(context, path):
    vcard_path = os.path.join(context.attachment_dir, path)
    if context.browser.driver_name == "ios":
        subprocess.call(
            ["xcrun", "simctl", "addmedia", context.browser.udid(), vcard_path]
        )
    else:
        name = context.persona["id"]
        emulator_id = get_android_emulator_id_from_name(name)
        check_output(
            ["adb", "-s", emulator_id, "push", vcard_path, "/sdcard/Download/"]
        )
        vcard_name = path.split("/")[1]
        check_output(
            [
                "adb",
                "-s",
                emulator_id,
                "shell",
                "am",
                "start",
                "-t",
                "text/x-vcard",
                "-d",
                "file:///sdcard/Download/" + vcard_name,
                "-a",
                "android.intent.action.VIEW",
                "com.android.contacts",
            ]
        )
        if context.browser.is_text_present("Allow Contacts to access", wait_time=2):
            context.execute_steps(u'When I press "Allow"')


@step(u"I install the app")
def install_app(context):
    if context.browser.driver_name == "ios":
        assert context.ios_app, u"No app specified"
        context.browser.driver.install_app(context.ios_app)
        return
    elif context.browser.driver_name == "android":
        assert context.android_app, u"No app specified"
        context.browser.driver.install_app(context.android_app)
        return
    assert False, u"Not using a mobile device"


@step(u"I toggle the TouchId enrollment")
def enroll_touch_id(context):
    context.browser.driver.toggle_touch_id_enrollment()


@step(u"I match the TouchID fingerprint")
def match_touch_id(context):
    if context.browser.driver_name == "ios":
        context.browser.driver.touch_id(True)
    elif context.browser.driver_name == "android":
        context.browser.driver.finger_print(1)
    else:
        assert False, u"Not using a mobile device"


@step(u"I mismatch the TouchID fingerprint")
def mismatch_touch_id(context):
    if context.browser.driver_name == "ios":
        context.browser.driver.touch_id(False)
    elif context.browser.driver_name == "android":
        assert False, u"Fingerprint mismatch not supported on android"
    else:
        assert False, u"Not using a mobile device"

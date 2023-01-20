import arcpy

from platform_api import auth_token, pas


class Login(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Login"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        usernameParam = arcpy.Parameter(
            displayName="Username",
            name="username",
            datatype="GPString",
            direction="input",
            parameterType="required"
        )

        passwordParam = arcpy.Parameter(
            displayName="Password",
            name="password",
            datatype="GPStringHidden",
            direction="input",
            parameterType="required"
        )

        return [
            usernameParam,
            passwordParam
        ]

    def execute(self, parameters, messages):
        """The source code of the tool."""
        messages.addMessage("Logging in...")

        resp = pas.login(
            username=parameters[0].valueAsText,
            password=parameters[1].valueAsText
        )

        if resp.ok:
            auth_token.token = resp.json()["access_token"]
            messages.addMessage("Logged In!")
        else:
            messages.addErrorMessage({
                "status_code": resp.status_code,
                "reason": resp.reason
            })

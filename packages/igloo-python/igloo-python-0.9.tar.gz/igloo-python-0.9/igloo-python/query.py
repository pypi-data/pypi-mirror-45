from .models.user import User
from .models.permanent_token import PermanentToken
from .models.pending_environment_share import PendingEnvironmentShare
from .models.environment import Environment
from .models.device import Device
from .models.float_value import FloatValue
from .models.pending_owner_change import PendingOwnerChange
from .models.notification import Notification
from .models.boolean_value import BooleanValue
from .models.string_value import StringValue
from .models.float_series_value import FloatSeriesValue
from .models.category_series_value import CategorySeriesValue
from .models.category_series_node import CategorySeriesNode
from .models.file_value import FileValue
from .models.float_series_node import FloatSeriesNode


class QueryRoot:
    def __init__(self, client):
        self.client = client

    @property
    def user(self):
        return User(self.client)

    def environment(self, id):
        return Environment(self.client, id)

    def device(self, id):
        return Device(self.client, id)

    def floatValue(self, id):
        return FloatValue(self.client, id)

    def stringValue(self, id):
        return StringValue(self.client, id)

    def booleanValue(self, id):
        return BooleanValue(self.client, id)

    def fileValue(self, id):
        return FileValue(self.client, id)

    def floatSeriesValue(self, id):
        return FloatSeriesValue(self.client, id)

    def categorySeriesValue(self, id):
        return CategorySeriesValue(self.client, id)

    def pendingEnvironmentShare(self, id):
        return PendingEnvironmentShare(self.client, id)

    def pendingOwnerChange(self, id):
        return PendingOwnerChange(self.client, id)

    def permanentToken(self, id):
        return PermanentToken(self.client, id)

    def notification(self, id):
        return Notification(self.client, id)

    def floatSeriesNode(self, id):
        return FloatSeriesNode(self.client, id)

    def categorySeriesNode(self, id):
        return CategorySeriesNode(self.client, id)

    def getNewTotpSecret(self):
        return self.client.query("{getNewTotpSecret{secret,qrCode}}", keys=["getNewTotpSecret"])

    def getWebAuthnEnableChallenge(self):
        return self.client.query("{getWebAuthnEnableChallenge{publicKeyOptions,jwtChallenge}}", keys=["getWebAuthnEnableChallenge"])

    def getWebAuthnLogInChallenge(self, email):
        return self.client.query('{getWebAuthnLogInChallenge(email:"%s"){publicKeyOptions,jwtChallenge}}' % email, keys=["getWebAuthnLogInChallenge"])

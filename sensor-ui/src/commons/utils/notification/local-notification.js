import {LocalNotifications} from "@capacitor/local-notifications";
import {PushNotifications} from "@capacitor/push-notifications";

const localNotification = {
    async getPermission() {
        await LocalNotifications.requestPermissions().then().catch();
    },

    subscribeActionPerformedEvt(eventHandler) {
        return LocalNotifications.addListener('localNotificationActionPerformed', eventHandler);
    },

    subscribeNotificationReceivedEvt(eventHandler) {
        return LocalNotifications.addListener('localNotificationReceived', eventHandler);
    },

    async enable() {
        await this.getPermission();
    },
    async schedule(options) {
        await LocalNotifications.schedule(options);
    }



};

export default localNotification;

import {PushNotifications} from "@capacitor/push-notifications";
import { FCM } from "@capacitor-community/fcm";
import {App} from "@capacitor/app";

const pushNotification = {

    getPermission(resultHandler, errorHandler) {
        return PushNotifications.requestPermissions().then(async result => {
            if (result.receive === 'granted') {
                await PushNotifications.register();
                return resultHandler(result)
            } else {
                return errorHandler(result)
            }
        });
    },

    subscribeRegistrationEvt(eventHandler) {
        return PushNotifications.addListener('registration', eventHandler);
    },
    subscribeRegistrationErrorEvt(eventHandler) {
        return PushNotifications.addListener('registrationError', eventHandler);
    },

    subscribeActionPerformedEvt(eventHandler) {
        return PushNotifications.addListener('pushNotificationActionPerformed', eventHandler);
    },

    subscribeNotificationReceivedEvt(eventHandler) {
        return PushNotifications.addListener('pushNotificationReceived', eventHandler);
    },

    async enable() {
        const handler = (data) => {};
        await this.getPermission(handler, handler);
        await this.subscribeRegistrationEvt(handler);
        await this.subscribeRegistrationErrorEvt(handler);
    },

    async subscribeTopic(topic, eventHandler, errorHandler) {
        await FCM.subscribeTo({ topic })
            .then(eventHandler)
            .catch(errorHandler);
    },

    async receiveNotification(localNotificationScheduler) {
        await this.subscribeNotificationReceivedEvt(
            async (notification) => {
                const {isActive} = await App.getState()
                if (isActive) {
                    await localNotificationScheduler({
                        notifications: [{
                            title: notification.title,
                            body: notification.body,
                            id: parseInt(notification.id),
                            data: notification.data,
                            schedule: {at: new Date(Date.now() + 1000 * 5)},
                            sound: null,
                            attachments: null,
                            actionTypeId: '',
                            extra: null,
                        }],
                    });
                }
            }).catch(alert);
    }
};

export default pushNotification;

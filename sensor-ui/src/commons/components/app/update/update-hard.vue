<template>
    <fv-container>
        <q-card class="update-card">
            <q-card-section>
                <div>
                    <strong>প্রিয়,</strong>
                    <div>লজেন্স অ্যাপে কিছু গুরুত্বপূর্ণ নতুন পরিবর্তন এসেছে। অনুগ্রহপূর্বক এখনি আপডেট করুন।</div>
                </div>
            </q-card-section>

            <q-card-actions align="right" class="q-gutter-sm q-mr-xs q-mb-xs">
                <a-btn label="EXIT" neutral tertiary @click="exitApp"/>
                <a-btn action label="UPDATE NOW" primary @click="openStoreURL"/>
            </q-card-actions>
        </q-card>
    </fv-container>
</template>

<script>
import {openURL as utilOpenURL} from 'quasar'
import {App} from '@capacitor/app'

export default {
    name: "update-hard",
    data() {
        return {
            googleStoreLink: 'https://play.google.com/store/apps/details?id=com.peddlecloud.lojens',
            appleStoreLink: ''
        }
    },
    methods: {
        exitApp() {
            App.exitApp();
        },
        openStoreURL() {
            let storeLink = undefined;
            if (this.$q.platform.is.android) storeLink = this.googleStoreLink;
            else if (this.$q.platform.is.ios) storeLink = this.appleStoreLink;
            utilOpenURL(storeLink);
        },
    }
}
</script>

<style scoped>

</style>

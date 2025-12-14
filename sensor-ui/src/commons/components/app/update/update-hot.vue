<template>
    <fv-container>
        <q-card class="update-card">
            <q-card-section>
                <div>
                    <strong>প্রিয়,</strong>
                    <div>লজেন্স অ্যাপে নতুন পরিবর্তন এসেছে। অনুগ্রহপূর্বক একটু অপেক্ষা করুন । আপডেট ডাউনলোড হচ্ছে ...
                    </div>
                    <a-spinner padding-clz="q-pa-sm"/>
                </div>
            </q-card-section>
        </q-card>
    </fv-container>
</template>

<script>
import {CapacitorUpdater} from "capacitor-updater";

export default {
    name: "update-hot",
    methods: {
        async updateApp() {
            const url = 'https://update.lojens.com/update.zip';
            try {
                const updaterVersion = await CapacitorUpdater.download({url});
                await CapacitorUpdater.set({version: updaterVersion.version});
                await this.$ovsAppUpdate.syncVersion();
                await this.$ovsAppUpdate.resetTryCount();
                await CapacitorUpdater.reload();
            } catch (e) {
                await this.$ovsAppUpdate.incrementTryCount();
                await CapacitorUpdater.reload();
            }
        }
    },
    async mounted() {
        await this.updateApp();
    }
}
</script>

<style scoped>

</style>

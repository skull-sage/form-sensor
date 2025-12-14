<template>
    <a-field :label="label">
        <template #control>
            <span v-if="value">{{$lDateTime(value)}}</span>
        </template>
        <template v-slot:prepend>
            <q-icon name="r_event" class="cursor-pointer">
                <q-popup-proxy transition-show="scale" transition-hide="scale">
                    <q-date v-model="date" @input="emitDaTime()" mask="MM/DD/YYYY" minimal>
                        <div class="row items-center justify-end">
                            <q-btn v-close-popup label="Close" color="primary" flat />
                        </div>
                    </q-date>
                </q-popup-proxy>
            </q-icon>
        </template>

        <template v-slot:append>
            <q-icon name="r_access_time" class="cursor-pointer">
                <q-popup-proxy transition-show="scale" transition-hide="scale">
                    <q-time v-model="time" @input="emitDaTime()" mask="HH:mm">
                        <div class="row items-center justify-end">
                            <q-btn v-close-popup label="Close" color="primary" flat />
                        </div>
                    </q-time>
                </q-popup-proxy>
            </q-icon>
        </template>
    </a-field>
</template>

<script>
export default {
    name: "a-date-input",
    props: {
        label: String,
        value: [Date, String], // if string then ISO Format
        emitIso: Boolean, // if true then will emit ISO else emit Date
    }, //['value', 'label', 'emitISO' ],

    data() {
        return {
            date: '',
            time: ''
        }
    },
    mounted() {
        this.calcDaTime();
    },
    methods:{
        calcDaTime() {
            let date;

            if (this.value === undefined)
                date = new Date();
            else if (this.value instanceof Date == false)
                date = new Date(this.value);
            else
                date = this.value;

            let year = date.getFullYear();
            let month = date.getMonth() + 1;
            let monthDay = date.getDate();
            let hour = date.getHours();
            let min = date.getMinutes();
            this.date = `${month}/${monthDay}/${year}`;
            this.time = `${hour}:${min}`;

            //  this.$emit('input', date.toISOString());

        },

        emitDaTime() {
            let dateParts = this.date.split('/')
            let month = Number.parseInt(dateParts[0]) - 1;
            let day = Number.parseInt(dateParts[1]);
            let year = Number.parseInt(dateParts[2]);

            let timeParts = this.time.split(':');
            let hours = Number.parseInt(timeParts[0]);
            let minutes = Number.parseInt(timeParts[1]);

            let resultDate = new Date(year, month, day, hours, minutes);
            if (this.emitIso)
                this.$emit('input', resultDate.toISOString());
            else
                this.$emit('input', resultDate);

        }


    },

}
</script>

<style scoped>

</style>

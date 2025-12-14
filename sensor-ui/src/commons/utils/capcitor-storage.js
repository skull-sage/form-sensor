import {Storage} from "@capacitor/storage";

const setValue = async (key, value) => {
    await Storage.set({key: key, value: value});
};

const getValue = async (key) => {
    const {value} = await Storage.get({key: key});
    return value;
};

const getIntValue = async (key) => {
    const {value} = await Storage.get({key: key});
    return parseInt(value);
};

const setIntValue = async (key, value) => {
    await Storage.set({key: key, value: value.toString()});
};

export default {
    setValue,
    getValue,
    getIntValue,
    setIntValue
};

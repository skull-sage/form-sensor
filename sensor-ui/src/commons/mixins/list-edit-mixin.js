
import utilCloneDeep from 'lodash/cloneDeep';

export default {

    data(){
      return {
        dataList: [],
        sequence : 0
      }
    },
    watch:{
      'value.length':{ // external push/delete
        handler(new$, old$){
            this.initDataList()
        },
        immediate: true
      }
    },
    props: {
      value : Array,
      nextId: {
        type: Function,
        default: function (){
         return ++this.sequence
        }
      }
    },

    methods:{

      initSeq(){
        if(this.value){
          this.value.forEach((item$) => {
            if(this.sequence < item$.id)
              this.sequence = item$.id;
          });
        }
      },
      initDataList(){
         this.initSeq();
        if(this.value){
          let wrapList = [];
          this.value.forEach((item$) => {
            if(!item$.id)
              item$.id = this.nextId();
            wrapList.push(item$);
          });
          this.dataList = wrapList;

        }
      },

      push(val$, idx$)
      {
        if(!idx$)
          this.dataList.push(val$);
        else
          this.dataList.splice(idx$, 1, val$);

        this.emitList();
      },

      removeAt(idx$){
        this.dataList.splice(idx$, 1);
        this.$nextTick(()=> this.emitList());
      },
      emitList(){
        this.$emit('input', this.dataList);
      },
      updateOrder(list$){
        this.dataList = list$;
        this.$emit('input', this.dataList);
      }
    }
}

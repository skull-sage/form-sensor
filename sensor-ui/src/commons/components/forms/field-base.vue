
<script>
export default {

  props:{
    accent: Boolean,
    color: {
      type: String,
      default: 'blue-grey-9'
    },
    lazyRules: {
      type: Boolean,
      default: true
    },
    rules: Array // [ f(val$) -> Boolean/PromiseBoolean || errMsg: 'That failed for this reason']
  },
  data(){
    return {
       errMsg: undefined
    }
  },
  mounted() {
    if(this.lazyRules)
      return;
     this.validate(this.$attrs.value);
  },
  computed:{

    calcErrorMsg(){
      return this.errMsg || this.$attrs['error-message'];
    },

    focusStyle(){
        if(this.accent)
          return 'indigo-6';
        else
          return 'grey-5';
      }

  },
  methods:
    {

      validate(val$){
        //this.error = false;
        this.errMsg = undefined;

        if(!this.rules) return;
      //  if(val$ === '' || val$ === undefined) return;
        //debugger;
        for(const rule of this.rules)
        {
          let ruleVal = rule(val$); // true for validated, false if invalid

          if(typeof ruleVal === 'string')
          {

            this.errMsg = ruleVal
            this.$emit('update:error-message', this.errMsg);
            return;
          }

        }

        this.$emit('update:error-message', this.errMsg);

      }
    }
}
</script>


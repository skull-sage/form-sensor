<template>
  <div v-intersection="intersectionConfig" >
    <slot></slot>
    <!--<transition :enter-active-class="enterClz" v-if="transition">
      <div  class="full-width" :key="triggerKey" >
        <slot></slot>
      </div>
    </transition>
    <slot v-else></slot>-->
  </div>
</template>

<script>
  import {calcElmBox} from 'src/commons/utils/dom-util'
  import ANIME from 'animejs'

  export default {
    name: "a-scroll-interact",
    props: {
      rootElm : {
        type: Object,
        default: null,
      },
      rootMargin: {
        type: String,
        default: '-20px 0px -20px 0px'
      },
      // will require to add emitting intersectionRatio too later
      /*threshold: {
        type: Number,
        default: 1.0
      },*/
      enterOnly: {
        type : Boolean,
        default: true
      },
      transition : {
        type : Boolean,
        default: false
      },
      animationClz : {
        type: String,
        default: 'bounceIn'
      }

    },
    data()
    {
      return {
        triggerKey : 0,
        prevRatio : 0,
        triggered: false
      }
    },
    mounted(){
      this.$nextTick(this.fixHeight);
    },
    updated() {
      this.$nextTick(this.fixHeight)
    },
    computed:
    {
      enterClz(){
        return 'animated '+ this.animationClz
      },
      intersectionConfig()
      {
        return {
          handler: (entry$)=>
          {


            if(this.enterOnly)
            {
              if(entry$.isIntersecting)
              {

                this.triggerKey++;
                this.$emit("enter",  this.triggerKey);
                if(this.transition && this.triggered == false)
                  this.animate();
              }
            }
            else
            {
              this.triggerKey++;
              if(entry$.isIntersecting)
              {
                this.$emit("enter",  this.triggerKey);
              }
              else
              {
                this.$emit("exit", this.triggerKey);
              }
            }

          } ,
          cfg: {
            // any options from "Intersection observer options"
            // on https://developer.mozilla.org/en-US/docs/Web/API/Intersection_Observer_API
            root: this.rootElm, // DOM Element
            rootMargin: this.rootMargin,
            threshold: 1.0
          }
        }

      }

    },

    methods:
    {
      animate(){

        this.triggered = true;
        let domChild = this.$el.firstChild;
        domChild.classList.add('animated', 'bounceIn');


        setTimeout(()=> {
          this.triggered = false;
          domChild.classList.remove('animated', 'bounceIn');
        }, 1100)

        //domChild.
        /*let animeTL = ANIME.timeline();
          animeTL.add({
            targets: domChild,
            scaleY: 1.1,
            duration: 400,
            /!*easing: 'easeOutInBounce '*!/
            easing: 'cubic-bezier(0.755, 0.05, 0.855, 0.06)'
          }).add({
            targets: domChild,
            scaleY: 1.05,
            duration: 300,
            /!*easing: 'easeOutInBounce '*!/
            easing: 'cubic-bezier(0.215, 0.61, 0.355, 1)'
          }).add({
            targets: domChild,
            scaleY: 1,
            duration: 200,
            easing: 'linear'
          });*/
      },
      fixHeight()
      {
        let box = calcElmBox(this.$el);
        this.$el.style.height = box.offsetHeight+'px';
        this.$el.style.width = box.offsetWidth+'px';
        this.$el.style.overflow = 'visible';
      }
    }


  }
</script>

<style scoped>


  .animated
  {
    animation-duration:  1s;
  }
</style>

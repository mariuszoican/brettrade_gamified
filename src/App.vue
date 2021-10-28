<template>
  <v-app app>
    <v-overlay :value="showHappyFace">
      <div class="d-flex flex-column align-center justify-center">
        <img
          src="https://i.gifer.com/7cIs.gif"
          alt=""
          height="300px"
          width="300px"
        />
        <h1>We are so happy to see back!</h1>
      </div>
    </v-overlay>
    <div class="funnyam d-flex flex-column">
      <transition
        name="custom-classes-transition"
        enter-active-class="animate__animated animate__bounceIn"
        appear
      >
        <speech-bubble :text="lastMsg" v-if="showLastMsg"> </speech-bubble>
      </transition>
      <img
        src="https://i.gifer.com/XOsX.gif"
        alt=""
        height="100px"
        width="100px"
        style="align-self:flex-end"
      />
    </div>
    <transition name="fade">
      <particles-bg
        v-if="snackbar"
        :config="pconfig"
        :type="particle_type"
        :bg="false"
        :canvas="{ position: 'absolute', zIndex: 1000, top: 0, left: 0 }"
      />
    </transition>
    <input type="hidden" :value="currentPrice" name="exit_price" />
    <v-app-bar app clipped-left>
      <v-sheet outlined class="d-flex align-center ml-1 pa-2 rounded-xl">
        <div class="d-flex align-center  font-weight-bold ">
          Current price:
          <div class="ml-1 pa-2 red   white--text text-no-wrap rounded-pill">
            ${{ formattedTween || currentPrice }}
          </div>
        </div>
      </v-sheet>

      <v-spacer></v-spacer>
      <v-btn @click="dialog = true">Sell</v-btn>
    </v-app-bar>
    <end-dialog :dialog="showEndDialog" @finishGame="finishGame"></end-dialog>

    <confirm-dialog
      :dialog="dialog"
      :currentPrice="currentPrice"
      @sell="sell"
      @continueKeeping="continueKeeping"
    ></confirm-dialog>
    <v-navigation-drawer clipped app width="300" color="blue" permanent>
      <v-card
        class="d-flex flex-column buysellcard"
        fill-height
        style="height:100%"
      >
        <v-card-text class="overflow-y-auto" style="margin-bottom:50px">
          <v-list>
            <v-list-item-group active-class="border" color="indigo" class=" ">
              <v-list-item
                class="m-3  "
                v-for="(item, i) in messages"
                :key="i"
                :id="`li_${i}`"
                :ref="`li_${i}`"
                dense
              >
                <v-list-item-content
                  class="message pr-3 "
                  v-breathing-colors="sample"
                >
                  <v-list-item-title
                    class="titlestyle"
                    style=" white-space:pre-wrap;"
                  >
                    <typical
                      class="typicalWrapper"
                      :steps="[`${item}`, 1000]"
                      :loop="1"
                      :wrapper="'div'"
                    ></typical>
                  </v-list-item-title>
                </v-list-item-content>
              </v-list-item>
            </v-list-item-group>
          </v-list>
          <div id="listend" ref="listend">&nbsp</div>
        </v-card-text>
      </v-card>
    </v-navigation-drawer>
    <v-main app v-show="true">
      <v-container fluid>
        <v-row>
          <v-col cols="12">
            <highcharts
              :constructorType="'stockChart'"
              class="hc"
              :options="chartOptions"
              ref="priceGraph"
              :updateArgs="[true, true, true]"
            ></highcharts>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
    <v-snackbar v-model="snackbar">
      {{ snackbartext }}

      <template v-slot:action="{ attrs }">
        <v-btn color="pink" text v-bind="attrs" @click="snackbar = false">
          Close
        </v-btn>
      </template>
    </v-snackbar>
  </v-app>
</template>

<script>
/* eslint-disable */
import icon from "./assets/icon.js";
import typical from "vue-typical";
import { ParticlesBg } from "particles-bg-vue";
import SpeechBubble from "./components/SpeechBubble.vue";
import EndDialog from "./components/EndDialog";
import ConfirmDialog from "./components/ConfirmDialog";
import { Chart } from "highcharts-vue";
import { differenceInSeconds, addSeconds, getTime } from "date-fns";
import gsap from "gsap";
import _ from "lodash";
import add from "date-fns/fp/add/index.js";

const maxPrices = 100;
const startingPrice = 100;
const tickFrequency = 3;

const formatDown = {
  color: "red",
  icon: "mdi-arrow-down-bold",
};
const formatUp = {
  color: "green darken-3",
  icon: "mdi-arrow-up-bold",
};
const numToStr = {
  1: "One",
  2: "Two",
  3: "Three",
  4: "Four",
  5: "Five",
  6: "Six",
  7: "Seven",
  8: "Eight",
  9: "Nine",
  10: "Ten",
};
export default {
  name: "App",
  components: {
    highcharts: Chart,
    ConfirmDialog,
    EndDialog,
    typical,
    ParticlesBg,
    SpeechBubble,
  },
  data: function() {
    const minx = Date.UTC(2009, 0, 1);
 
    const maxx = getTime(addSeconds(new Date, tickFrequency*maxPrices))
    console.debug(maxx,'jopa')
    return {
      minx,
      maxx,
      showHappyFace: false,
      showLastMsg: false,
      particle_type: "fountain",
      heartConfig: {
        num: [4, 7],
        rps: 0.1,
        radius: [5, 40],
        life: [1.5, 3],
        v: [2, 3],
        tha: [-30, 30],
        body: icon,
        alpha: [0.6, 0],
        scale: [0.1, 0.4],
        position: "all",
        cross: "dead",
        random: 1,
      },
      snackbar: false,
      snackbartext: null,
      happyHappens: false,
      prices: [],
      sample: {
        colors: ["red", "green", "blue"],
        interval: 3000,
        transition: {
          duration: 1000,
        },
      },
      showEndDialog: false,
      messages: [],
      zeroCounter: 0, //bad, all this is bad. TODO
      grownCounter: 0,
      TwoTwosCounter: 0,
      sensitivity: 5,
      sensitivity2: 3,
      probToZero: 0.001,
      startingPrice,
      currentPrice: startingPrice,
      submittable: false,
      onPause: false,
      startTime: new Date(),
      endTime: null,
      timeSpent: null,
      reset: false,
      dialog: false,
      tweenedPrice: null,
      stockInterval: null,
      tickFrequency,
      chartOptions: {
        time: { useUTC: false },
        yAxis: {startOnTick: false,
      endOnTick: false,},
        xAxis: {startOnTick: false,
      endOnTick: false,
      showLastLabel: true,
          min: getTime(new Date()),
          max:getTime(addSeconds(new Date, tickFrequency*maxPrices))},
        navigator: { enabled: false },
        rangeSelector: {
          enabled:false,
          inputEnabled: false,
          selected: 0,
        },
        series: [
          {
            data: [[getTime(new Date()), startingPrice]],
          },
        ],
      },
    };
  },
  computed: {
    lastMsg() {
      return _.last(this.messages);
    },
    pconfig() {
      if (this.particle_type == "fountain") return {};
      return this.heartConfig;
    },
    formattedTween() {
      if (this.tweenedPrice) return this.tweenedPrice.toFixed(2);
      return this.currentPrice.toFixed(2);
    },
  },
  watch: {
    dialog(v) {
      this.onPause = v;
    },
    messages(v) {
      this.showLastMsg = true;
      setTimeout(() => {
        this.showLastMsg = false;
      }, 3000);
    },
    prices(v) {
      if (v.length % 10 === 0) {
        this.messages.push(
          `You keep doing this ALREADY for ${v.length} price updates! That's the spirit!`
        );
      }
      if (v.length >= maxPrices) {
        this.submittable = true;
      }
    },
    zeroCounter(v) {
      if (v === this.sensitivity) {
        this.messages.push("Ouch! Why it takes so long to grow!!!");
        this.zeroCounter = 0;
      }
    },
    grownCounter(v) {
      if (v === this.sensitivity) {
        const msg = `Wow! ${
          numToStr[this.sensitivity]
        } straight price growths in a row! To the sky!`;
        this.messages.push(msg);
        this.snackbartext = `Wow! ${
          numToStr[this.sensitivity]
        } straight price growths in a row! To the sky!`;
        this.snackbar = true;
        setTimeout(() => {
          this.snackbar = false;
        }, 3000);
        this.grownCounter = 0;
      }
    },
    TwoTwosCounter(v) {
      if (v === this.sensitivity2) {
        const msg = `That's insane! ${
          numToStr[this.sensitivity2]
        } 2s in a row! You gonna be rich!`;
        this.snackbartext = msg;
        this.particle_type = "custom";
        this.snackbar = true;
        setTimeout(() => {
          this.snackbar = false;
          this.particle_type = "fountain";
        }, 3000);
        this.messages.push(msg);
        this.TwoTwosCounter = 0;
      }
    },
    async submittable(val) {
      if (val) {
        await this.sendMessage({ name: "Trade_ends" });
        this.showEndDialog = true;
        this.onPause = true;
        // document.getElementById("form").submit();
      }
    },
    currentPrice: function(newValue) {
      this.$refs.listend.scrollIntoView({ behavior: "smooth" });

      gsap.to(this.$data, {
        duration: 0.5,
        tweenedPrice: newValue,
        onUpdate: this.tweenUpd,
      });
    },
  },
  async created() {},
  async mounted() {
    this.messages.push("Hello!");
    this.$nextTick(() => {
      this.$refs.listend.scrollIntoView({ behavior: "smooth" });
      
      this.$refs.priceGraph.chart.setSize(null, window.innerHeight - 100);
      // this.$refs.priceGraph.chart.reflow();
    });
 
    this.stockInterval = setInterval(async () => {
      if (!this.onPause) {
        const addendum = _.random(0, 2);
        this.currentPrice += addendum;
        const r = _.random(0, 1, true);
        if (r < this.probToZero) {
          this.submittable = true;
          this.currentPrice = 0;
        }
        this.addMessage(this.currentPrice, addendum);
        this.prices.push(this.currentPrice);
        
        this.chartOptions.series[0].data.push([
          getTime(new Date()),
          this.currentPrice,
        ]);
        
      }
    }, this.tickFrequency * 1000);
  },
  methods: {
    finishGame() {
      console.log("game finished");
    },
    addMessage(price, addendum) {
      // bad structure. let's think about it later
      if (price === 0) {
        const msg = `Game ends!`;
        this.messages.push(msg);
      }
      if (addendum === 0 && !this.onPause) {
        this.zeroCounter++;
        this.TwoTwosCounter = 0;
        this.grownCounter = 0;
      }
      if (addendum > 0 && !this.onPause) {
        this.zeroCounter = 0;
        this.grownCounter++;
        if (addendum == 2) {
          this.TwoTwosCounter++;
        }
      }
    },
    async sendMessage(obj) {},
    tweenUpd(v) {
      this.tweenedPrice = _.round(this.tweenedPrice, 2);
    },

    async sell() {
      await this.sendMessage({ name: "Sell" });
      this.dialog = false;
      this.submittable = true;
      this.onPause = true;
    },

    async continueKeeping() {
      await this.sendMessage({ name: "continueKeeping" });
      this.dialog = false;
      this.submittable = false;

      this.showHappyFace = true;
      setTimeout(() => {
        this.showHappyFace = false;
        this.onPause = False;
      }, 2000);
    },
  },
};
</script>

<style>
#app {
  background: rgba(0, 0, 0, 0);
  /* font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px; */
}
.word-break {
  word-break: break-word;
}
.titlestyle {
  padding-left: 10px;
  margin-left: 20px;
  white-space: pre-wrap;
}
.message {
  padding-left: 10px;
  margin-left: 20px;
  white-space: normal;

  font-family: "Open Sans", sans-serif;
  box-sizing: border-box;
  position: relative;
  max-width: 400px;
  padding: 6px 15px;

  font-size: 12px;
  word-break: break-word;
  color: #fff;
  border: none;
  background-color: rgb(0, 153, 255);
  border-radius: 20px;
}
.listouter1 {
  height: 100%;
  display: flex;
  flex-direction: column;
}
.listouter2 {
  flex: 1 1 auto;
  display: flex;
  flex-direction: column;
  /* flex-direction: column-reverse; */
  overflow-y: scroll;
}
.canvas {
  z-index: 1000;
}
.fade-enter-active,
.fade-leave-active {
  transition: opacity 1s;
}
.fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
  opacity: 0;
}
.funnyam {
  position: fixed;
  z-index: 1000;
  bottom: 10px;
  right: 10px;
}
</style>

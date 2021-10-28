<template>
  <v-app app>
    <input type="hidden" :value="currentPrice" name="exit_price" />
    <v-app-bar app clipped-left>
      <v-sheet outlined class="d-flex align-center ml-1 pa-2 rounded-xl">
        <div class="d-flex align-center  font-weight-bold ">
          Current price:
          <div class="ml-1 pa-2 red   white--text text-no-wrap rounded-pill">
            ${{ tweenedPrice || currentPrice }}
          </div>
        </div>
      </v-sheet>

      <v-spacer></v-spacer>
      <v-btn @click="dialog = true">Sell</v-btn>
    </v-app-bar>
    <end-dialog
      :dialog="showEndDialog"
      @finishGame='finishGame'
      
    ></end-dialog>

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
            <v-list-item-group active-class="border" color="indigo">
              <v-list-item
                v-for="(item, i) in messages"
                :key="i"
                :id="`li_${i}`"
                :ref="`li_${i}`"
                dense
              >
                <v-list-item-content>
                  <v-list-item-title v-text="item"></v-list-item-title>
                </v-list-item-content>
              </v-list-item>
            </v-list-item-group>
          </v-list>
          <div id="listend" ref="listend">&nbsp</div>
        </v-card-text>
      </v-card>
    </v-navigation-drawer>
    <v-main app>
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
  </v-app>
</template>

<script>
/* eslint-disable */


import EndDialog from "./components/EndDialog";
import ConfirmDialog from "./components/ConfirmDialog";
import { Chart } from "highcharts-vue";
import { differenceInSeconds } from "date-fns";
import gsap from "gsap";
import _ from "lodash";
import add from "date-fns/fp/add/index.js";

const formatDown = {
  color: "red",
  icon: "mdi-arrow-down-bold",
};
const formatUp = {
  color: "green darken-3",
  icon: "mdi-arrow-up-bold",
};

export default {
  name: "App",
  components: {
    highcharts: Chart,
    ConfirmDialog,
    EndDialog
  },
  data: function() {
    return {
      showEndDialog:false,
      messages: [],
      probToZero: 0.1,
      startingPrice: 100,
      currentPrice: 100,
      submittable: false,
      startTime: new Date(),
      endTime: null,
      timeSpent: null,
      reset: false,
      dialog: false,
      tweenedPrice: null,
      stockInterval: null,
      tickFrequency: 1,
      chartOptions: {
        xAxis: {
          max: 100,
          ordinal: false,
        },
        yAxis: {},
        navigator: { enabled: false },
        rangeSelector: {
          inputEnabled: false,
          selected: false,
        },
        series: [
          {
            data: [100],
          },
        ],
      },
    };
  },
  computed: {
    formattedTween() {
      return this.tweenedPrice.toFixed(2);
    },
  },
  watch: {
    async submittable(val) {
      if (val) {
        await this.sendMessage({ name: "Trade_ends" });
        this.showEndDialog=true;
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
    this.$nextTick(() => {
      this.$refs.listend.scrollIntoView({ behavior: "smooth" });

      this.$refs.priceGraph.chart.setSize(null, window.innerHeight - 150);
      // this.$refs.priceGraph.chart.reflow();
    });
    this.stockInterval = setInterval(async () => {
      if (!this.dialog && !this.submittable) {
        const addendum = _.random(0, 2);
        this.currentPrice += addendum;
        const r = _.random(0, 1, true);
        if (r < this.probToZero) {
          this.submittable = true;
          this.currentPrice = 0;
        }
        this.addMessage(this.currentPrice, addendum);

        this.chartOptions.series[0].data.push(this.currentPrice);
      }
    }, this.tickFrequency * 1000);
  },
  methods: {
    finishGame(){
      console.log('game finished')
    },
    addMessage(price, addendum) {
      if (price === 0) {
        const msg = `Game ends!`;
        this.messages.push(msg);
      }
      if (addendum > 0 && !this.dialog && !this.submittable) {
        const msg = `Price growth: + ${addendum}`;
        this.messages.push(msg);
      }
    },
    async sendMessage(obj) {},
    tweenUpd(v) {
      this.tweenedPrice = _.round(this.tweenedPrice, 2);
    },
    innerShowDialog() {
      this.dialog = true;
    },

    async sell() {
      await this.sendMessage({ name: "Sell" });
      this.dialog = false;
      this.submittable = true;
    },

    async continueKeeping() {
      await this.sendMessage({ name: "continueKeeping" });
      this.dialog = false;
      this.submittable = false;
    },
  },
};
</script>

<style>
#app {
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
</style>

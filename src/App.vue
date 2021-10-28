<template>
  <v-app>
    <input type="hidden" :value="currentPrice" name="exit_price" />
    <v-app-bar app  >
      <v-card elevation="4" v-if="currentPrice"   min-width="200">
        <v-card-title>
          <span class="word-break">Current price:</span>
        </v-card-title>
        <v-card-text class="text-h5 font-weight-bold">
          <h2>
            {{ tweenedPrice || currentPrice }}
          </h2>
        </v-card-text>
      </v-card>
      <v-spacer></v-spacer>
      <v-btn @click="dialog=true">Sell</v-btn>
    </v-app-bar>
    <confirm-dialog
      :dialog="dialog"
      :currentPrice="currentPrice"
      @sell="sell"
      @continueKeeping="continueKeeping"
    ></confirm-dialog>
    <v-main>
      <v-container fluid>
        <v-row>
          <v-col cols="12">
            <highcharts
              :constructorType="'stockChart'"
              class="hc"
              :options="chartOptions"
              ref="chart1"
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


import ConfirmDialog from "./components/ConfirmDialog";
import { Chart } from "highcharts-vue";
import { differenceInSeconds } from "date-fns";
import gsap from "gsap";
import _ from "lodash";

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
  },
  data: function() {
    return {
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
      tickFrequency: 3,
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
        // await this.sendMessage({ name: "Trade_ends" });
        // document.getElementById("form").submit();
      }
    },
    currentPrice: function(newValue) {
      gsap.to(this.$data, {
        duration: 0.5,
        tweenedPrice: newValue,
        onUpdate: this.tweenUpd,
      });
    },
  },
  async created() {
    this.$options.sockets.onopen = async () =>
      await this.sendMessage({ name: "Trade_starts" });
    this.$options.sockets.onmessage = (data) => console.log(data);
  },
  async mounted() {
    this.stockInterval = setInterval(async () => {
      if (!this.dialog) {
        const addendum = _.random(0, 2);
        this.currentPrice+=addendum
        this.chartOptions.series[0].data.push(this.currentPrice);
      }
    }, this.tickFrequency * 2000);
  },
  methods: {
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
      this.submittable = true;
    },
  },
};
</script>

<style>
#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
.word-break {
  word-break: break-word;
}
</style>

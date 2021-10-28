<template>
  <v-dialog v-model="dialog" max-width="600">
    <v-card>
      <v-card-title class="text-h5">Selling decision</v-card-title>

      <v-card-text>
        Do you really want to sell your asset? If you click 'Sell' this round will be over.
      </v-card-text>

      <v-card-actions>
        <v-spacer></v-spacer>
        <div  >
          <v-btn-toggle>
            <v-btn color="green darken-1" @click="continueKeeping">
              Keep
            </v-btn>

            <v-btn color="red darken-1" @click="sell"> Sell</v-btn>
          </v-btn-toggle>
        </div>
        
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
 
export default {
  props: ["dialog", "currentPrice"],
  components: {
   
  },
  data: () => ({   }),

  methods: {
    async conditionalSelling(val) {
      if (this.$socket.readyState == 1) {
        const obj = {
          name: "slider value changed",
          sliderValue: val,
          currentPrice: this.currentPrice,
        };
        await this.$socket.sendObj(obj);
      }

      if (val == 0) {
        this.sell();
      }
    },
    sell() {
      this.$emit("sell");
    },
    continueKeeping() {
      this.$emit("continueKeeping");
    },
  },
};
</script>

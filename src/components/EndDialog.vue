<template>
  <v-dialog v-model="dialog" persistent max-width="490">
    <v-card>
      <v-card-title class="text-h5" color="danger"
        >End of the round</v-card-title
      >

      <v-card-text>
        Click 'Next' to continue to the next round
      </v-card-text>

      <v-card-actions>
        <v-spacer></v-spacer>
         
          
            <v-btn color="red darken-1" @click="submit"> Next</v-btn>
           
        
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  props: ["dialog"],
  components: {},
  data: () => ({}),

  methods: {
    submit() {
      this.$emit("finishGame");
    },
  },
};
</script>

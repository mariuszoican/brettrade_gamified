module.exports = {
  publicPath: process.env.NODE_ENV === "production" ? "/crossmerged/" : "/",
  lintOnSave: false,
  transpileDependencies: ["vuetify"],
};

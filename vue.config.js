module.exports = {
  publicPath:
    process.env.NODE_ENV === "production" ? "/brettrade_gamified/" : "/",
  lintOnSave: false,
  transpileDependencies: ["vuetify"],
};

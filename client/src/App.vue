<template>
  <div id="app">
    <el-container>
      <el-header>
        <el-menu background-color="#545c64" mode="horizontal">
          <el-menu-item index="1">流量分析系统</el-menu-item>
        </el-menu>
      </el-header>
      <el-container>
        <el-aside width="200px">
          <el-menu default-active="2">
            <el-menu-item index="2" @click="$router.push('/monitor')">
              <i class="el-icon-view"></i>
              <span slot="title">实时监控</span>
            </el-menu-item>
            <el-menu-item index="3" @click="$router.push('/analyser')">
              <i class="el-icon-info"></i>
              <span slot="title">数据分析</span>
            </el-menu-item>
            <el-menu-item index="4" @click="$router.push('setting')">
              <i class="el-icon-setting"></i>
              <span slot="title">设置</span>
            </el-menu-item>
          </el-menu>
        </el-aside>
        <el-main>
          <router-view></router-view>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>

export default {
  name: 'app',
  mounted: function () {
    console.log(this.$route)
  }
}
</script>

<style lang="scss">
@import "./assets/css/common.scss";
body {
  margin: 0;
  padding: 0;
  .el-header {
    padding: 0;
  }
}
</style>

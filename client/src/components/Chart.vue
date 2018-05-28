<template>
  <el-col :span="12">
    <el-row>
      <el-form ref="form" label-width="100px">
        <el-form-item label="查询类别">
          <el-select size="mini" v-model="currentStatisticTypeIdx" placeholder="请选择">
            <el-option v-for="(opt,idx) in seletOptions" :key="opt.value" :label="opt.name" :value="idx">
            </el-option>
          </el-select>
        </el-form-item>
      </el-form>
    </el-row>
    <el-row class="chart-container">
      <IEcharts @click="handlePieClick" :option="ratioOption" />
    </el-row>
  </el-col>
</template>
<script>
import IEcharts from 'vue-echarts-v3/src/full.js'
export default {
  name: 'Chart',
  components: {
    IEcharts
  },
  mounted () {
    this.loadDist()
  },
  watch: {
    currentStatisticTypeIdx: function () {
      this.loadDist()
    }
  },
  props: ['seletOptions', 'title'],
  data () {
    return {
      dist: [],
      currentStatisticTypeIdx: 0
    }
  },
  computed: {
    ratioOption: function () {
      let legend = []
      for (let idx in this.dist) {
        legend.push(this.dist[idx].name)
      }
      return {
        backgroundColor: '#2c343c',
        title: {
          text: this.title,
          left: 'center',
          top: 20,
          textStyle: {
            color: '#ccc'
          }
        },
        legend: {
          type: 'scroll',
          orient: 'vertical',
          right: 10,
          top: 20,
          bottom: 20,
          data: legend,
          textStyle: {
            color: '#ccc'
          }
        },
        series: [
          {
            type: 'pie',
            radius: '55%',
            center: ['40%', '50%'],
            data: this.dist,
            label: {
              normal: {
                textStyle: {
                  color: 'rgba(255, 255, 255, 0.3)'
                }
              }
            }
          }
        ]
      }
    }
  },
  methods: {
    // 读取分布数据
    loadDist: function () {
      let vm = this
      vm.dist = []
      vm.$http.get('/api/dist/' + vm.seletOptions[vm.currentStatisticTypeIdx].value)
        .then((response) => {
          for (let idx in response.data) {
            let item = response.data[idx]
            vm.dist.push({
              value: item._v,
              name: item._k
            })
          }
        })
        .catch((e) => {
          console.error(e)
          this.$message.error('网络错误！')
        })
    },
    handlePieClick: function (event, instance, ECharts) {
      console.log(arguments)
    }
  }
}
</script>
<style lang="scss" scoped>
.chart-container {
  height: 320px;
}
</style>

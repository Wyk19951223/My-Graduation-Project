<template>
  <el-row>
    <el-row>
      <el-col :span="14">
        <el-form ref="form" label-width="100px">
          <el-form-item label="查询类别">
            <el-select size="mini" v-model="currentStatisticTypeIdx" placeholder="请选择">
              <el-option v-for="(opt,idx) in seletOptions" :key="opt.value" :label="opt.name" :value="idx">
              </el-option>
            </el-select>
          </el-form-item>
        </el-form>
      </el-col>
      <el-col :span="10">
        <el-switch class="flow-type-switch" v-model="flowDataType" active-text="按数据包统计" inactive-text="按流量统计">
        </el-switch>
      </el-col>
    </el-row>
    <el-row>
      <el-col :span="12">
        <el-row class="chart-container">
          <IEcharts @click="handlePieClick" :option="ratioOption" />
        </el-row>
      </el-col>
      <el-col :span="11">
        <el-row class="chart-container">
          <IEcharts :option="trendOption" />
        </el-row>
      </el-col>
    </el-row>
  </el-row>
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
      currentStatisticTypeIdx: 0,
      currentSeriesData: [[], []],
      currentValue: null,
      flowDataType: true
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
    },
    trendOption: function () {
      return {
        title: {
          text: this.currentValue,
          left: 'center',
          top: 20,
          textStyle: {
            color: '#ccc'
          }
        },
        dataZoom: [
          {
            id: 'dataZoomX_s',
            type: 'slider',
            xAxisIndex: [0],
            filterMode: 'none'
          },
          {
            id: 'dataZoomX_i',
            type: 'inside',
            xAxisIndex: [0],
            filterMode: 'none'
          },
          {
            id: 'dataZoomY',
            type: 'slider',
            yAxisIndex: [0],
            filterMode: 'none'
          }
        ],
        xAxis: {
          data: [],
          type: 'value',
          name: '时间'
        },
        yAxis: {
          type: 'value',
          name: this.flowDataType ? '数据包数量' : '流量'
        },
        series: [{
          symbolSize: 2,
          data: this.flowDataType ? this.currentSeriesData[0] : this.currentSeriesData[1],
          type: 'line'
        }],
        animation: false
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
          // 转换为echarts识别的格式
          for (let idx in response.data) {
            let item = response.data[idx]
            if (vm.seletOptions[0].value === 'src_ip' || vm.seletOptions[0].value === 'dst_ip') {
              if (item._v > 100) {
                vm.dist.push({
                  value: item._v,
                  name: item._k
                })
              }
            } else if (vm.seletOptions[0].value === 'protocol') {
              vm.dist.push({
                value: item._v,
                name: item._k
              })
            } else {
              if (item._v > 80) {
                vm.dist.push({
                  value: item._v,
                  name: item._k
                })
              }
            }
          }
        })
        .catch((e) => {
          console.error(e)
          this.$message.error('网络错误！')
        })
    },
    handlePieClick: function (event, instance, ECharts) {
      // 处理点击饼图的事件 请求对应类别的字段的值等于选中值的情况
      let vm = this
      // 第一维是包数量 第二维是流量
      vm.currentSeriesData = [[], []]
      vm.currentValue = event.data.name
      vm.$http.get('/api/series/' + vm.seletOptions[vm.currentStatisticTypeIdx].value + '/' + vm.currentValue)
        .then((response) => {
          for (let idx in response.data) {
            let packet = response.data[idx]
            // 将数据点添加到分布图中
            vm.currentSeriesData[0].push(
              [packet.last_updated, packet.packetcount]
            )
            vm.currentSeriesData[1].push(
              [packet.last_updated, packet.octetcount]
            )
          }
          console.log(response)
        })
        .catch((e) => {
          console.error(e)
          this.$message.error('网络错误！')
        })
      console.log(event.data.name)
    }
  }
}
</script>
<style lang="scss" scoped>
.chart-container {
  height: 350px;
}
.flow-type-switch {
  margin-top: 10px;
}
</style>

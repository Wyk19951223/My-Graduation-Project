<template>
  <div>
    <el-row :gutter="10">
      <el-col :span="14">
        <el-card>
          <div slot="header" class="clearfix">
            <span>统计信息</span>
          </div>
          <el-row>
            <el-col :span="14">
              <el-form ref="form" label-width="100px">
                <el-form-item label="查询协议">
                  <el-select size="mini" v-model="statisticProtocolType" placeholder="选择协议">
                    <el-option v-for="protocol in protocols" :key="protocol.value" :label="protocol.value" :value="protocol.value">
                    </el-option>
                  </el-select>
                </el-form-item>
              </el-form>
            </el-col>
            <el-col :span="10">
              <el-switch v-model="flowDataType" active-text="按数据包统计" inactive-text="按流量统计">
              </el-switch>
            </el-col>
          </el-row>
          <el-row>
            <el-form ref="form" label-width="100px">
              <el-form-item label="起止时间">
                <el-input type="number" class="query-time" size="mini" v-model="flowDataRange[0]" placeholder="起始"></el-input>
                <el-input type="number" class="query-time" size="mini" v-model="flowDataRange[1]" placeholder="终止"></el-input>
              </el-form-item>
            </el-form>
          </el-row>
          <el-row class="chart-container">
            <IEcharts :option="flowOption" />
          </el-row>
        </el-card>
      </el-col>
      <el-col :span="10">
        <el-card class="box-card">
          <div slot="header" class="clearfix">
            <span>异常流量</span>
          </div>
          <el-table :data="abnormalFlow" height="350">
            <el-table-column prop="last_updated" label="时间">
            </el-table-column>
            <el-table-column prop="protocol" label="协议">
            </el-table-column>
            <el-table-column prop="packetcount" label="数据包大小">
            </el-table-column>
            <el-table-column prop="octetcount" label="流量大小(Byte)">
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>
    <el-row class="mt-10" :gutter="20">
      <el-col>
        <el-card>
          <div slot="header" class="clearfix">
            <span>实时流量监控</span>
          </div>
          <el-table :highlight-current-row="true" @current-change="handleCurrentChange" :data="realtimeData" :default-sort="{prop: 'last_updated', order: 'descending'}" height="300" max-height="350">
            <el-table-column prop="last_updated" label="时间" align="center" sortable>
            </el-table-column>
            <el-table-column prop="protocol" label="协议 " align="center" width="220" :filters="protocols" :filter-method="protocolFilter" filter-placement="bottom-end">
            </el-table-column>
            <el-table-column prop="src_ip" label="源IP地址" align="center">
            </el-table-column>
            <el-table-column prop="src_port" label="源端口" align="center">
            </el-table-column>
            <el-table-column prop="dst_ip" label="目的IP地址" align="center">
            </el-table-column>
            <el-table-column prop="dst_port" label="目的端口" align="center">
            </el-table-column>
            <el-table-column prop="hash_id" label="HASH ID" align="center">
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>
    <el-row v-if="currentPacket">
      <el-col>
        <el-card class="detail-info">
          <div slot="header" class="clearfix">
            <span>
              <small>详细信息</small>
            </span>
          </div>
          <el-row>
            <strong>时刻: </strong>{{ currentPacket.last_updated }}s
          </el-row>
          <el-row>
            <strong>ID: </strong>{{ currentPacket.id }}
          </el-row>
          <el-row>
            <strong>HASH ID: </strong>{{ currentPacket.hash_id }}
          </el-row>
          <el-row>
            <strong>协议: </strong>
            <el-tag type="success">{{ currentPacket.protocol }}</el-tag>
          </el-row>
          <el-row>
            <strong>packetcount: </strong>{{ currentPacket.packetcount }}
          </el-row>
          <el-row>
            <strong>octetcount: </strong>{{ currentPacket.octetcount }}
          </el-row>
          <el-row>
            <el-col :span="12">
              <strong>源MAC地址: </strong>{{ currentPacket.src_mac }}
            </el-col>
            <el-col :span="12">
              <strong>目的MAC地址: </strong>{{ currentPacket.dst_mac }}
            </el-col>
          </el-row>
          <el-row>
            <el-col :span="12">
              <strong>源IP地址: </strong>{{ currentPacket.src_ip }}
            </el-col>
            <el-col :span="12">
              <strong>源端口号: </strong>{{ currentPacket.src_port }}
            </el-col>
          </el-row>
          <el-row>
            <el-col :span="12">
              <strong>目的IP地址: </strong>{{ currentPacket.dst_ip }}
            </el-col>
            <el-col :span="12">
              <strong>目的端口号: </strong>{{ currentPacket.dst_port }}
            </el-col>
          </el-row>
          <el-row>
            <el-col :span="12">
              <strong>flow_start: </strong>{{ currentPacket.flow_start }}
            </el-col>
            <el-col :span="12">
              <strong>flow_end: </strong>{{ currentPacket.flow_end }}
            </el-col>
          </el-row>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>
<script>
import IEcharts from 'vue-echarts-v3/src/full.js'
export default {
  name: 'monitor',
  components: {
    IEcharts
  },
  data () {
    return {
      statisticProtocolType: '',
      protocols: [],
      flowDataType: false,
      flowDataRange: [0, 1000],
      realtimeData: [],
      currentPacket: null
    }
  },
  computed: {
    flowOption: function () {
      // 统计信息展示框
      let vm = this
      let dataPoints = []
      for (let idx in vm.realtimeData) {
        let packet = vm.realtimeData[idx]
        // 选择指定区间
        if (packet.last_updated >= vm.flowDataRange[0] && packet.last_updated <= vm.flowDataRange[1]) {
          // 统计对应协议类型的信息
          if (vm.statisticProtocolType === packet.protocol) {
            // 选择统计流量还是包
            if (vm.flowDataType) {
              dataPoints.push([packet.last_updated, packet.packetcount])
            } else {
              dataPoints.push([packet.last_updated, packet.octetcount])
            }
          }
        }
      }
      return {
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
          // min: vm.flowDataRange[0],
          // max: vm.flowDataRange[1]
        },
        yAxis: {
          type: 'value'
        },
        series: [{
          symbolSize: 5,
          data: dataPoints,
          type: 'line'
        }]
      }
    },
    abnormalFlow: function () {
      let vm = this
      let abnormalFlowList = []
      let packetThs = 5000
      let octetThs = 5000
      // 检测异常流量
      for (let idx in vm.realtimeData) {
        if (vm.realtimeData[idx].packetcount > packetThs || vm.realtimeData[idx].octetcount > octetThs) {
          abnormalFlowList.push(vm.realtimeData[idx])
        }
      }
      return abnormalFlowList
    }
  },
  mounted () {
    let vm = this
    vm.$http.get('/api/flowdata')
      .then((response) => {
        vm.realtimeData = response.data.packets
        for (let idx in response.data.protocols) {
          vm.protocols.push({
            text: response.data.protocols[idx],
            value: response.data.protocols[idx]
          })
          if (vm.protocols.length) {
            vm.statisticProtocolType = vm.protocols[0].value
          }
        }
      })
      .catch((e) => {
        console.error(e)
        this.$message.error('网络错误！')
      })
  },
  methods: {
    protocolFilter: function (value, row) {
      return row.protocol === value
    },
    handleCurrentChange (row, oldRow) {
      this.currentPacket = row
    }
  }
}
</script>
<style lang="scss" scoped>
.chart-container {
  height: 320px;
}
.el-form-item {
  margin-bottom: 3px;
  .query-time {
    width: 80px;
  }
}
.detail-info {
  .el-row {
    padding-top: 10px;
    padding-bottom: 10px;
    padding-left: 10px;
    border-bottom: 1px solid #eee;
  }
}
</style>

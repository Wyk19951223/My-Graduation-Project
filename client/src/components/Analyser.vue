<template>
  <div>
    <el-row>
      <el-card>
        <div slot="header" class="clearfix">
          <span>历史流量</span>
        </div>
        <el-table :highlight-current-row="true" :data="flowData" :default-sort="{prop: 'last_updated', order: 'ascending'}" height="300" max-height="350">
          <el-table-column prop="last_updated" label="时间" align="center" sortable>
          </el-table-column>
          <el-table-column prop="protocol" label="协议 " align="center" width="220" :filters="filters.protocols" :filter-method="filterHandler" filter-placement="bottom-end">
          </el-table-column>
          <el-table-column prop="src_ip" label="源IP地址" align="center" :filters="filters.src_ips" :filter-method="filterHandler" width="130px">
          </el-table-column>
          <el-table-column prop="src_port" label="源端口" align="center" :filters="filters.src_ports" :filter-method="filterHandler">
          </el-table-column>
          <el-table-column prop="dst_ip" label="目的IP地址" align="center" :filters="filters.dst_ips" :filter-method="filterHandler" width="130px">
          </el-table-column>
          <el-table-column prop="dst_port" label="目的端口" align="center" :filters="filters.dst_ports" :filter-method="filterHandler">
          </el-table-column>
          <el-table-column prop="packetcount" label="包数量" align="center" sortable>
          </el-table-column>
          <el-table-column prop="octetcount" label="流量大小" align="center" sortable width="100px">
          </el-table-column>
          <el-table-column prop="hash_id" label="HASH ID" align="center">
          </el-table-column>
        </el-table>
      </el-card>
    </el-row>
    <el-row class="mt-10">
      <el-card>
        <div slot="header" class="clearfix">
          <span>异常流量统计</span>
        </div>
        <el-table :highlight-current-row="true" :data="abnormalFlowData" :default-sort="{prop: 'last_updated', order: 'ascending'}" height="300" max-height="350">
          <el-table-column prop="last_updated" label="时间" align="center" sortable>
          </el-table-column>
          <el-table-column prop="protocol" label="协议 " align="center" width="220" :filters="filters.protocols" :filter-method="filterHandler" filter-placement="bottom-end">
          </el-table-column>
          <el-table-column prop="src_ip" label="源IP地址" align="center" :filters="filters.src_ips" :filter-method="filterHandler" width="130px">
          </el-table-column>
          <el-table-column prop="src_port" label="源端口" align="center" :filters="filters.src_ports" :filter-method="filterHandler">
          </el-table-column>
          <el-table-column prop="dst_ip" label="目的IP地址" align="center" :filters="filters.dst_ips" :filter-method="filterHandler" width="130px">
          </el-table-column>
          <el-table-column prop="dst_port" label="目的端口" align="center" :filters="filters.dst_ports" :filter-method="filterHandler">
          </el-table-column>
          <el-table-column prop="packetcount" label="包数量" align="center" sortable>
          </el-table-column>
          <el-table-column prop="octetcount" label="流量大小" align="center" sortable width="100px">
          </el-table-column>
          <el-table-column prop="hash_id" label="HASH ID" align="center">
          </el-table-column>
        </el-table>
      </el-card>
    </el-row>
    <el-row class="mt-10">
      <el-card>
        <div slot="header" class="clearfix">
          <span>IP地址分类统计</span>
        </div>
        <Chart :title="'IP地址分类统计'" :selet-options="[{value: 'src_ip',name: '源IP地址'},{value: 'dst_ip',name: '目的IP地址'}]" />
      </el-card>
    </el-row>
    <el-row class="mt-10">
      <el-card>
        <div slot="header" class="clearfix">
          <span>端口分类统计</span>
        </div>
        <Chart :title="'端口分类统计'" :selet-options="[{value: 'src_port',name: '源端口'},{value: 'dst_port',name: '目的端口'}]" />
      </el-card>
    </el-row>
    <el-row class="mt-10">
      <el-card>
        <div slot="header" class="clearfix">
          <span>MAC地址分类统计</span>
        </div>
        <Chart :title="'MAC地址分类统计'" :selet-options="[{value: 'src_mac',name: '源MAC地址'},{value: 'dst_mac',name: '目的MAC地址'}]" />
      </el-card>
    </el-row>
    <el-row class="mt-10">
      <el-card>
        <div slot="header" class="clearfix">
          <span>协议流量分类统计</span>
        </div>
        <Chart :title="'协议分类统计'" :selet-options="[{value: 'protocol',name: '所有协议'}]" />
      </el-card>
    </el-row>
  </div>
</template>
<script>
import Chart from './Chart.vue'
export default {
  name: 'analyser',
  components: {
    Chart
  },
  data: function () {
    return {
      flowData: null,
      filters: {
        protocols: [],
        src_ips: [],
        dst_ips: [],
        src_ports: [],
        dst_ports: []
      },
      filterOptions: ['protocols', 'src_ips', 'dst_ips', 'src_ports', 'dst_ports']
    }
  },
  computed: {
    abnormalFlowData: function () {
      let vm = this
      let abnormalFlowList = []
      let packetThs = 5000
      let octetThs = 5000
      for (let idx in vm.flowData) {
        if (vm.flowData[idx].packetcount > packetThs || vm.flowData[idx].octetcount > octetThs) {
          abnormalFlowList.push(vm.flowData[idx])
        }
      }
      return abnormalFlowList
    }
  },
  mounted () {
    let vm = this
    vm.$http.get('/api/flowdata')
      .then((response) => {
        vm.flowData = response.data.packets
        vm.buildFilters(response.data.filters)
      })
      .catch((e) => {
        console.error(e)
        this.$message.error('网络错误！')
      })
  },
  methods: {
    buildFilters: function (filters) {
      console.log(filters)
      let vm = this
      // 获取过滤条件
      for (let filterId in vm.filterOptions) {
        // 当前过滤条件
        let filterName = vm.filterOptions[filterId]
        for (let idx in filters[filterName]) {
          // 将当前过滤条件离散值添加到vm的过滤条件中
          vm.filters[filterName].push({
            text: filters[filterName][idx],
            value: filters[filterName][idx]
          })
        }
      }
    },
    filterHandler: function (value, row, column) {
      return row[column.property] === value
    }
  }
}
</script>
<style lang="scss" scoped>
</style>

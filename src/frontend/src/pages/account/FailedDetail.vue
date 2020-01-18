<template>
  <main-layout :crumbs="[{
    title: '用户管理',
    path: '/account/list'
  }, {
    title: '用户导入结果'
  }]">
    <div class="row aligin-right">
      <div class="col-lg-12">
        <div class="ibox">
          <div class="ibox-title">
            <h5>{{task.name}}</h5>
          </div>
          <div class="ibox-content">
            <div class="row m-b-sm">
              <div class="col-lg-12">
                <span class="m-r-sm">
                  任务状态: <label class="fa fa-circle text-navy">完成</label>
                </span>
                <span class="m-r-sm">
                  成功插入: <label>{{task.result ? task.result.success : 0}}</label> 条数据
                </span>
                <span>
                  插入失败: <label>{{task.result ? task.result.failed : 0}}</label> 条数据
                </span>
              </div>
            </div>
            <div class="table-responsive">
              <el-table :data="failedRecord" @sort-change="sort = { key: $event.prop, order: $event.order }" tooltip-effect="light" style="width: 100%" :default-sort = "{prop: 'line', order: 'ascending'}">
                <el-table-column prop="line" sortable label="Line Number" width="120"></el-table-column>
                <el-table-column prop="sheet" sortable label="Sheet Name" width="120"></el-table-column>
                <el-table-column prop="msg" label="Error Message" show-overflow-tooltip></el-table-column>
              </el-table>
            </div>
            <div class="row m-t-sm m-r-sm">
              <div class="col-lg-12">
                <el-pagination
                  @size-change="page = 1"
                  :page-sizes="[10, 20, 50, 100]"
                  layout="total, sizes, prev, pager, next, jumper"
                  :total="totalCount"
                  :page-size.sync="pageSize"
                  :current-page.sync="page">
                </el-pagination>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </main-layout>
</template>

<script>
export default {
  name: 'account-create',
  data: () => ({
    task: {},
    page: 1,
    pageSize: 10,
    sort: {
      key: 'line',
      order: false
    }
  }),
  computed: {
    failedRecord () {
      if (!this.task.result) {
        return []
      }
      let record = this.task.result.failed_record
      record = record.sort((r1, r2) => this.compare(r1, r2))
      let startIndex = (this.page - 1) * this.pageSize
      return record.slice(startIndex, startIndex + this.pageSize)
    },
    totalCount () {
      return this.task.result ? this.task.result.failed_record.length : 0
    }
  },
  async created () {
    let id = this.$route.params.id
    this.task = await this.$axios.get(`task/${id}`)
  },
  methods: {
    compare (r1, r2) {
      let sort = this.sort
      if (sort.order === 'descending') {
        return r1[sort.key] > r2[sort.key]
          ? -1
          : r1[sort.key] < r2[sort.key]
            ? 1
            : 0
      } else if (sort.order === 'ascending') {
        return r1[sort.key] < r2[sort.key]
          ? -1
          : r1[sort.key] > r2[sort.key]
            ? 1
            : 0
      } else {
        return 0
      }
    }
  }
}
</script>

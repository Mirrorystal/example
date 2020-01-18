<template>
  <main-layout>
    <div class="row">
      <div class="col-lg-12">
        <div class="ibox">
          <div class="ibox-title">
            <h5>用户列表</h5>
          </div>
          <div class="ibox-content">
            <div class="row">
              <div class="col-sm-4">
                <div class="input-group align-left">
                  <el-input v-model="condition.searchKey" class="handle-input m-r-sm" clearable placeholder="用户名/邮箱"></el-input>
                  <el-button @click="fetchUserList()" type="primary" icon="el-icon-search">用户搜索</el-button>
                </div>
              </div>
            </div>
            <div class="row">
              <div class="col-sm-3 m-b-xs">
                <div class="input-group align-between">
                    <el-select @change="fetchUserList()" class="handle-select" v-model.trim="condition.department" placeholder="所有部门">
                      <el-option
                        v-for="item in decorateDepartments"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value">
                      </el-option>
                    </el-select>
                    <el-select @change="fetchUserList()" class="handle-select" v-model.trim="condition.position" placeholder="所有职位">
                      <el-option
                        v-for="item in decoratePositions"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value">
                      </el-option>
                    </el-select>
                </div>
              </div>
            </div>
            <div class="row">
              <div class="col-sm-4 m-b-xs">
                <div class="dropdown-group pull-left">
                  <el-dropdown split-button type="primary">
                    选择操作
                    <el-dropdown-menu slot="dropdown">
                      <el-dropdown-item @click.native="handleDelete">删除用户</el-dropdown-item>
                      <el-dropdown-item @click.native="handleReset">重置密码</el-dropdown-item>
                      <el-dropdown-item @click.native="handleElevate">升级为管理员</el-dropdown-item>
                      <el-dropdown-item @click.native="handleDemote">降级为普通用户</el-dropdown-item>
                    </el-dropdown-menu>
                  </el-dropdown>
                </div>
                <router-link to="/account/create"><el-button type="primary" plain> 添加用户</el-button></router-link>
              </div>
              <div class="col-sm-4"></div>
              <div class="col-sm-4 m-b-xs excel-group">
                <el-upload
                  action="/api/account/user/import"
                  :headers="headers"
                  :show-file-list="false"
                  list-type="picture"
                  :on-success="uploadSuccess"
                  accept="application/vnd.ms-excel,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet">
                  <el-dropdown @command="downloadTemplateFile" class="m-r-sm" split-button type="primary">
                    excel导入用户
                    <el-dropdown-menu slot="dropdown">
                      <el-dropdown-item>下载Excel模板</el-dropdown-item>
                    </el-dropdown-menu>
                  </el-dropdown>
                  <el-button type="primary" @click.stop="exportUsers">导出用户到excel</el-button>
                </el-upload>
              </div>
            </div>
            <div class="table-responsive">
              <el-table :data="userList" tooltip-effect="light" style="width: 100%" :default-sort = "{prop: 'username', order: 'ascending'}"
                @selection-change="handleSelectionChange">
                <el-table-column type="selection" width="55"></el-table-column>
                <el-table-column prop="username" sortable label="姓名" width="120" show-overflow-tooltip></el-table-column>
                <el-table-column prop="email" label="邮箱" width="120" show-overflow-tooltip></el-table-column>
                <el-table-column prop="department" sortable label="部门" show-overflow-tooltip></el-table-column>
                <el-table-column prop="position" sortable label="职位" show-overflow-tooltip></el-table-column>
                <el-table-column prop="phone" label="电话" show-overflow-tooltip></el-table-column>
                <el-table-column prop="role" sortable label="权限" show-overflow-tooltip></el-table-column>
                <el-table-column prop="loginNum" sortable label="登录次数" show-overflow-tooltip></el-table-column>
                <el-table-column  fixed="right"  label="操作"  width="100">
                  <template slot-scope="scope">
                    <el-button @click="editUser(scope.row,scope.$index)" type="text" size="small"> 修改信息 </el-button>
                  </template>
                </el-table-column>
              </el-table>
              <el-dialog title="用户信息修改" :visible.sync="updateVisible" :modal="false" width="400px" center>
              <el-form :model="userInfo" :rules="rules" ref="userInfo" label-width="75px" size="small">
                <el-form-item label="姓名：" prop="username"><el-input  type="text" v-model.trim="userInfo.username" clearable></el-input></el-form-item>
                <el-form-item label="电话：" prop="phone"><el-input  v-model.trim="userInfo.phone" clearable></el-input></el-form-item>
                <el-form-item label="部门：" >
                  <el-select  v-model.trim="userInfo.department" placeholder="所在部门">
                    <el-option
                      v-for="item in decorateDepartments"
                      :key="item.value"
                      :label="item.label"
                      :value="item.value">
                    </el-option>
                  </el-select>
                </el-form-item>
                <el-form-item label="职位：">
                  <el-select   v-model.trim="userInfo.position" placeholder="所在职位">
                    <el-option
                      v-for="item in decoratePositions"
                      :key="item.value"
                      :label="item.label"
                      :value="item.value">
                    </el-option>
                  </el-select>
                </el-form-item>
                <el-form-item >
                  <el-button size="large" type="primary" @click="saveChanges('userInfo')">保存修改</el-button>
                  <el-button size="large" type="primary" @click="updateVisible = false">取消修改</el-button>
                </el-form-item>
              </el-form>
            </el-dialog>
            </div>
            <div class="row table-pagination m-t-xs m-r-xs">
              <el-pagination
                @size-change="fetchUserList()"
                @current-change="fetchUserList"
                @prev-click="fetchUserList(pagination.page - 1)"
                @next-click="fetchUserList(pagination.page + 1)"
                :page-sizes="[10, 20, 50, 100]"
                layout="total, sizes, prev, pager, next, jumper"
                :total="pagination.totalCount"
                :page-size.sync="pagination.pageSize"
                :current-page="pagination.page">
              </el-pagination>
            </div>
          </div>
        </div>
      </div>
    </div>
  </main-layout>
</template>

<script>
import { mapGetters, mapMutations, mapActions } from 'vuex'
import { sleep, download } from '@/utils/tools'
import { isEmpty } from 'element-ui/src/utils/util'

export default {
  name: 'account-list',
  created () {
    if (isEmpty(this.$store.getters.positions)) { this.fetchDepartAndPositions() }
  },
  data () {
    var validUsername = (rule, value, callback) => {
      const Usernamereg = /^[\u4e00-\u9fa5_a-zA-Z0-9_]{2,10}$/
      if (value === '') {
        callback(new Error('请输入用户名'))
      } else if (!Usernamereg.test(value)) {
        callback(
          new Error(
            '用户名不少于两个字符'
          )
        )
      } else {
        callback()
      }
    }
    var checkPhone = (rule, value, callback) => {
      const phoneReg = /^1[3|4|5|7|8][0-9]{9}$/
      if (!value) {
        return callback(new Error('电话号码不能为空'))
      }
      setTimeout(() => {
        if (!Number.isInteger(+value)) {
          callback(new Error('请输入数字值'))
        } else {
          if (phoneReg.test(value)) {
            callback()
          } else {
            callback(new Error('电话号码格式不正确'))
          }
        }
      }, 100)
    }
    return {
      userList: [],
      pagination: {
        page: 1,
        pageCount: 0,
        pageSize: 10,
        totalCount: 0
      },
      userSelection: [],
      userIds: [],
      dialogVisibleOfDelete: false,
      dialogVisibleOfReset: false,
      dialogVisibleOfElevate: false,
      dialogVisibleOfDemote: false,
      updateVisible: false,
      condition: {
        searchKey: '',
        department: '',
        position: ''
      },
      userInfo: {
        username: '',
        phone: '',
        department: '',
        position: ''
      },
      multipleSelection: [],
      id: '',
      rules: {
        username: [
          { validator: validUsername, trigger: 'blur' }
        ],
        phone: [
          { validator: checkPhone, trigger: 'blur' }
        ]
      }
    }
  },
  computed: {
    ...mapGetters(['headers']),
    decorateDepartments () {
      return this.$store.getters.departments.map((v) => { return { value: v, label: v } })
    },
    decoratePositions () {
      return this.$store.getters.positions.map((v) => { return { value: v, label: v } })
    }
  },
  mounted () {
    this.fetchUserList()
  },
  methods: {
    ...mapActions(['fetchDepartAndPositions']),
    ...mapMutations(['updateUserProfile']),
    editUser (item, idx) {
      this.userIndex = idx
      this.userInfo = {
        username: item.username,
        department: item.department,
        position: item.position,
        phone: item.phone
      }
      this.updateVisible = true
      var id = item.id
      this.id = id
      return id
    },
    saveChanges (userInfo) {
      this.updateVisible = false
      this.$refs[userInfo].validate(valid => {
        valid && this.$axios.put(`account/user/` + this.id, this.userInfo).then(() => {
          this.eventHub.$emit('change:user')
          return this.fetchUserList()
        }).then(() => {
          this.$message.success('修改成功')
        }).catch(error => {
          console.error(error)
          this.$message.error('修改失败')
        })
      })
    },
    uploadSuccess ({ taskId }) {
      taskId && this.showImportProgress(taskId)
    },
    async exportUsers () {
      let { taskId } = await this.$axios.get('account/user/export', {
        params: this.condition
      })
      taskId && this.showExportProgress(taskId)
    },
    downloadTemplateFile () {
      download('resource/task/user-template', '用户数据导入模板.xlsx')
    },
    async showImportProgress (taskId) {
      let progress = this.$progress.createProgress({
        title: '正在导入用户数据',
        percentage: 0,
        buttonText: false,
        comfirm: () => {
          this.$router.push({
            name: 'account-failed-detail',
            params: {
              id: taskId
            }
          })
        }
      })
      let task = null
      while (progress.percentage < 100) {
        task = await this.$axios.get(`task/result/${taskId}`)
        let { success = 0, failed = 0, total = 1 } = task
        if (total <= 0) {
          progress.percentage = 100
          break
        }
        progress.percentage = Math.floor((success + failed) / total * 100)
        progress.title = `正在导入用户数据, 失败: ${failed}`
        await sleep(500)
      }
      if (task.failed > 0) {
        progress.buttonText = '查看详情'
      }
      progress.title = `用户数据导入完成, 失败: ${task.failed}`
      this.eventHub.$emit('change:setting')
      this.eventHub.$emit('change:user')
    },
    async showExportProgress (taskId) {
      let progress = this.$progress.createProgress({
        title: '正在导出用户数据',
        percentage: 0,
        buttonText: '下载',
        comfirm: () => {
          download('resource/task/' + taskId, `导出用户数据 - ${new Date().getTime()}.xlsx`)
        },
        close: () => {
          this.$axios.delete(`task/${taskId}`)
        }
      })
      let task = null
      while (progress.percentage < 100) {
        task = await this.$axios.get(`task/result/${taskId}`)
        let { success = 0, total = 1 } = task
        if (total <= 0) {
          progress.percentage = 100
          break
        }
        progress.percentage = Math.floor(success / total * 100)
        await sleep(500)
      }
      progress.title = '用户数据导出完成'
    },
    handleDelete () {
      if (this.multipleSelection.length === 0) {
        this.$message.warning('您未选择想要删除的用户！')
      } else {
        this.$confirm('此操作将从列表中删除该用户, 是否继续?', '提示', {
          duration: 600,
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning',
          center: true
        }).then(() => {
          var userSelection = this.multipleSelection.map(user => user.id)
          return this.deleteUser(userSelection)
        })
      }
    },
    handleReset () {
      if (this.multipleSelection.length === 0) {
        this.$message.warning('您未选择想要重置密码的用户！')
      } else {
        this.$confirm('此操作将重置该用户密码, 是否继续?', '提示', {
          duration: 600,
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning',
          center: true
        }).then(() => {
          var userSelection = this.multipleSelection.map(function (item) {
            return item['id']
          })
          this.resetPassword(userSelection)
        })
      }
    },
    handleElevate () {
      if (this.multipleSelection.length === 0) {
        this.$message.warning('您未选择想要升级权限的用户！')
      } else {
        this.$confirm('此操作将升级该用户权限, 是否继续?', '提示', {
          duration: 600,
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning',
          center: true
        }).then(() => {
          var userSelection = this.multipleSelection.map(function (item) {
            return item['id']
          })
          this.elevateUser(userSelection)
        })
      }
    },
    handleDemote () {
      if (this.multipleSelection.length === 0) {
        this.$message.warning('您未选择想要降级权限的用户！')
      } else {
        this.$confirm('此操作将降级该用权限, 是否继续?', '提示', {
          duration: 600,
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning',
          center: true
        }).then(() => {
          var userSelection = this.multipleSelection.map(function (item) {
            return item['id']
          })
          this.demoteUser(userSelection)
        })
      }
    },
    handleSelectionChange (val) {
      this.multipleSelection = val
    },
    async deleteUser (userSelection) {
      try {
        await this.$axios.delete('account/users', {
          params: {
            userIds: userSelection
          }
        })
        this.eventHub.$emit('change:user')
        await this.fetchUserList()
        this.$message.success('删除成功')
      } catch (error) {
        this.$message.warning('用户不存在')
      }
    },
    async resetPassword (userSelection) {
      this.$axios.put('account/users/passwords', {
        ids: userSelection
      }).then(() => {
        this.$message.success('已成功重置密码！')
        this.fetchUserList()
      }).catch(error => {
        console.error(error)
        this.$message.warning('重置密码失败！')
      })
    },
    async elevateUser (userSelection) {
      this.$axios.put('account/users/permission', {
        ids: userSelection
      }).then(() => {
        this.$message.success('已成功升级权限！')
        this.fetchUserList()
      }).catch(error => {
        console.error(error)
        this.$message.warning('修改权限失败！')
      })
    },
    async demoteUser (userSelection) {
      this.$axios({
        url: 'account/users/permission',
        method: 'delete',
        params: {
          ids: userSelection
        }
      }).then(() => {
        this.$message.success('已成功降级权限！')
        this.fetchUserList()
      }).catch(error => {
        console.error(error)
        this.$message.warning('修改权限失败！')
      })
    },
    async fetchUserList (page = 1) {
      let result = await this.$axios.get('account/users', {
        params: {
          ...this.condition,
          page: page,
          pageSize: this.pagination.pageSize
        }
      })
      this.userList = this.formatUserList(result.items)
      this.pagination = result.meta
    },
    formatUserList (userList) {
      return userList.map(user => ({
        ...user,
        role: user.authorType > 0 ? '管理员' : '普通用户'
      }))
    }
  }
}
</script>

<style lang="scss">
.handle-select {
  width: calc((100% - 20px) / 2);
}
.handle-input {
  width: calc(100% - 83px);
}

.align-between {
  justify-content: space-between;
}

.align-left {
  justify-content: flex-start;
}

.table-pagination {
  text-align: right;
}

.input-group{
  padding: 2px 0 5px 0;
}

.dropdown-group{
  margin: 0 10px 2px 0;
}

</style>

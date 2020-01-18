<template>
  <main-layout>
    <div class="container-fluid">
      <div class="row  visible-lg visible-xl" >
        <div class=" text-center  col-4  col-lg-offset-1 col-lg-3   ">
          <el-form label-position="right" size="large"  :rules="rules" ref="userForm" :model="currentUser" label-width="100px">
            <el-form-item label="姓名：" prop="username" >
              <span  v-show="!edit">{{ currentUser.username }}</span>
              <el-input   v-show="edit" v-model.trim="currentUser.username"></el-input>
            </el-form-item>
            <el-form-item label="邮箱：" prop="email" >
              <span v-show="!edit">{{ currentUser.email }}</span>
              <el-input :readonly="true" suffix-icon=" "   v-show="edit" v-model.trim="currentUser.email"   align="center"></el-input>
            </el-form-item>
            <el-form-item label="部门：" prop="department">
              <span v-show="!edit">{{ currentUser.department }}</span>
              <el-select v-show="edit"  v-model.trim="currentUser.department" placeholder="请选择部门">
                <el-option
                  v-for="item in decorateDepartments"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value">
                </el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="职位：" prop="position">
              <span v-show="!edit">{{ currentUser.position }}</span>
              <el-select v-show="edit" v-model.trim="currentUser.position" placeholder="请选择职位">
                <el-option
                  v-for="item in decoratePositions"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value">
                </el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="电话：" prop="phone">
              <span v-show="!edit">{{ currentUser.phone }}</span>
              <el-input v-show="edit" v-model.trim="currentUser.phone"></el-input>
            </el-form-item>
            <el-form-item label="用户权限：" >
              <span >{{ currentUser.authorType > 0 ? '管理员' : '普通用户' }}</span>
            </el-form-item>
          </el-form>
          <div class="row"    type="flex" justify="center">
            <el-button  type="primary" @click="checkForm('userForm')">{{subText}}</el-button>
            <el-button type="primary" @click="dialogFormVisible = true">修改密码 </el-button>
            <el-dialog :modal="false"  title="用户密码修改" :visible="dialogFormVisible" width="33%" center>
              <el-form size="large" :model="passwords" :rules="rules" ref="PWDForm" label-width="100px">
<!--                <el-form-item label="请输入原密码" >-->
<!--                  <el-input show-password autofocus v-model.trim="passwords.oldPassword" autocomplete="off"></el-input>-->
<!--                </el-form-item>-->
                <el-form-item label="请输入新密码" prop="newPassword" >
                  <el-input show-password autofocus v-model.trim="passwords.newPassword" autocomplete="off"></el-input>
                </el-form-item>
                <el-form-item label="请确认新密码" >
                  <el-input show-password v-model.trim="passwords.confirmPass" autocomplete="off"></el-input>
                </el-form-item>

              </el-form>
              <div slot="footer" class="dialog-footer">
                <el-button @click="dialogFormVisible = false">取 消</el-button>
                <el-button type="primary" @click="changePassword('PWDForm')">确 定</el-button>
              </div>
            </el-dialog>
          </div>
        </div>
        <div  class="text-center col-4 col-sm-offset-2  col-sm-3 ">
          <el-dialog
            v-dialog-drag
            :modal="false"
            center
            title="选择头像"
            :visible.sync="selectAvatarDialogVisible"
            width="35%"
          >
            <div >
              <el-image
                :src="url"
                v-for="url in imageUrls"
                :key="url"
                class="m-l-xs"
                @click="handleClose(url)"  fit="fit" style="width: 100px; height: 100px"    >
                <div slot="placeholder"  class="image-slot">
                  加载中<span class="dot">...</span>
                </div>
              </el-image>
            </div>
          </el-dialog>
          <div @click="selectAvatarDialogVisible=true" class="m-t-lg">
            <el-avatar  :size="150" fit="fit" :src="currentUser.avatar">
              <img src="https://cube.elemecdn.com/e/fd/0fc7d20532fdaf769a25683617711png.png"/>
            </el-avatar>
          </div>
        </div>
      </div>
      <div class="row visible-sm  visible-md  visible-xs  " >
        <div  class="text-center col-6  ">
          <el-dialog
            v-dialog-drag
            :modal="false"
            center
            title="选择头像"
            :visible.sync="selectAvatarDialogVisible"
            width="30%"
          >
            <div>
              <el-image
                :src="url"
                v-for="url in imageUrls"
                :key="url"
                class="m-l-xs"
                @click="handleClose(url)"  fit="fit" style="width: 100px; height: 100px"    >
                <div slot="placeholder"  class="image-slot">
                  加载中<span class="dot">...</span>
                </div>
              </el-image>
            </div>
          </el-dialog>
          <div @click="selectAvatarDialogVisible=true" class="m-t-lg">
            <el-avatar  :size="150" fit="fit" :src="currentUser.avatar">
              <img src="https://cube.elemecdn.com/e/fd/0fc7d20532fdaf769a25683617711png.png"/>
            </el-avatar>
          </div>
        </div>
        <div class=" w-100  "></div>
        <div class=" text-center  col-6 col-sm-offset-2 col-sm-8  ">
          <el-form label-position="right"  :rules="rules" ref="userForm" :model="currentUser" label-width="100px">
            <el-form-item label="姓名：" prop="username" >
              <span  v-show="!edit">{{ currentUser.username }}</span>
              <el-input   v-show="edit" v-model.trim="currentUser.username"></el-input>
            </el-form-item>
            <el-form-item label="邮箱：" prop="email" >
              <span v-show="!edit">{{ currentUser.email }}</span>
              <el-input readonly   v-show="edit" v-model.trim="currentUser.email" placeholder="邮箱即为登录名" align="center"></el-input>
            </el-form-item>
            <el-form-item label="部门：" prop="department">
              <span v-show="!edit">{{ currentUser.department }}</span>
              <!--              <el-input   v-show="edit" v-model.trim="currentUser.department" placeholder="请选择所在部门" align="center"></el-input>-->
              <el-select v-show="edit"  v-model.trim="currentUser.department" placeholder="请选择">
                <el-option
                  v-for="item in decorateDepartments"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value">
                </el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="职位：" prop="position">
              <span v-show="!edit">{{ currentUser.position }}</span>
              <el-select v-show="edit" v-model.trim="currentUser.position" placeholder="请选择">
                <el-option
                  v-for="item in decoratePositions"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value">
                </el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="电话：" prop="phone">
              <span v-show="!edit">{{ currentUser.phone }}</span>
              <el-input v-show="edit" v-model.trim="currentUser.phone"></el-input>
            </el-form-item>
            <el-form-item label="用户权限：" >
              <span>{{ currentUser.authorType > 0 ? '管理员' : '普通用户' }}</span>
<!--              <el-input v-show="edit" :disabled="true" v-model="currentUser.authorType"></el-input>-->
            </el-form-item>
          </el-form>
          <div class="row"  type="flex" justify="center">
            <el-button  type="primary" @click="checkForm('userForm')">{{subText}}</el-button>
            <el-button type="primary" @click="dialogFormVisible = true">修改密码 </el-button>
            <el-dialog :modal="false"  title="用户密码修改" :visible="dialogFormVisible" width="33%" center>
              <el-form  size="large" :model="passwords" :rules="rules" ref="PWDForm" label-width="100px">
<!--                <el-form-item label="请输入原密码" >-->
<!--                  <el-input show-password autofocus v-model.trim="passwords.oldPassword" autocomplete="off"></el-input>-->
<!--                </el-form-item>-->
                <el-form-item label="请输入新密码" prop="newPassword" >
                  <el-input show-password autofocus v-model.trim="passwords.newPassword" autocomplete="off"></el-input>
                </el-form-item>
                <el-form-item label="请确认新密码" >
                  <el-input show-password v-model.trim="passwords.confirmPass" autocomplete="off"></el-input>
                </el-form-item>

              </el-form>
              <div slot="footer" class="dialog-footer">
                <el-button @click="dialogFormVisible = false">取 消</el-button>
                <el-button type="primary" @click="changePassword('PWDForm')">确 定</el-button>
              </div>
            </el-dialog>
          </div>
        </div>
      </div>
    </div>
  </main-layout>
</template>

<script>
import { mapActions, mapMutations } from 'vuex'
import { getHashFullPath } from '@/utils/url'
import { isObjectValueEqual } from '@/utils/tools'
import { isEmpty } from 'element-ui/src/utils/util'
export default {
  name: 'account-profile',
  created () {
    this.initData()
  },
  computed: {
    decorateDepartments () {
      return this.departments.map((v) => { return { value: v, label: v } })
    },
    decoratePositions () {
      return this.positions.map((v) => { return { value: v, label: v } })
    }
  },
  data () {
    return {
      passwords: {
        oldPassword: 'null',
        newPassword: '',
        confirmPass: ''
      },
      oldUser: Object,
      subText: '点击修改',
      edit: false,
      imageUrls: [require('@/assets/img/avatars/avatar1.png'), require('@/assets/img/avatars/avatar2.png'), require('@/assets/img/avatars/avatar5.png'), require('@/assets/img/avatars/avatar4.png'), require('@/assets/img/avatars/avatar3.png'), require('@/assets/img/avatars/avatar6.png'), require('@/assets/img/avatars/avatar7.png'), require('@/assets/img/avatars/avatar8.png')],
      selectAvatarDialogVisible: false,
      dialogTableVisible: false,
      dialogFormVisible: false,
      departments: [],
      positions: [],
      currentUser: {
        username: '',
        id: '',
        avatar: '',
        email: '',
        department: '',
        position: '',
        phone: '',
        authorType: 0
      },
      rules: {
        username: [
          { required: true, message: '此处不为空', trigger: 'blur' } ],
        email: [
          { required: true, message: '此处不为空', trigger: 'blur' },
          { type: 'email', message: '请输入正确的邮箱地址', trigger: ['blur', 'change'] }],
        departments: [
        ],
        positions: [
        ],
        phone: [
          { required: true, message: '此处不为空', trigger: 'blur' }],
        newPassword: [
          { min: 8, message: '密码长度不小与于8位', trigger: 'blur' }]
      }
    }
  },
  methods: {
    ...mapMutations(['updateUserProfile']),
    ...mapActions(['logout', 'fetchDepartAndPositions', 'submitForm', 'submitPasswordChange']),
    checkForm (formName) {
      if (!this.edit) {
        this.oldUser = Object.assign({}, this.currentUser)
        this.edit = !this.edit
        this.subText = '确定修改'
      } else {
        if (isObjectValueEqual(this.oldUser, this.currentUser)) {
          this.$message.warning('信息未修改')
          this.edit = !this.edit
          this.subText = '点击修改'
          return
        }
        this.$refs[formName].validate((valid) => {
          if (valid) {
            if (this.submitForm(this.currentUser)) { this.$message.success('修改成功') } else this.$message.error('修改失败')
            this.edit = !this.edit
            this.subText = '点击修改'
            return true
          } else return false
        })
      }
    },
    handleClose (url) {
      this.selectAvatarDialogVisible = false
      this.currentUser.avatar = url
      this.submitForm(this.currentUser) ? this.$message.success('头像修改成功') : this.$message.error('头像修改失败')
    },
    async initData () {
      if (this.$store.getters.currentUser != null) {
        Object.assign(this.currentUser, this.$store.getters.currentUser)
        if (isEmpty(this.$store.getters.positions)) { await this.fetchDepartAndPositions() }
        this.positions = this.$store.getters.positions
        this.departments = this.$store.getters.departments
      }
    },
    changePassword (formName) {
      if (!this.passwords.newPassword.length || !this.passwords.oldPassword.length || !this.passwords.confirmPass.length) return
      if (this.passwords.newPassword !== this.passwords.confirmPass) {
        this.$message.warning('两次密码不一致')
        return
      }
      if (this.passwords.newPassword === this.passwords.oldPassword) {
        this.$message.warning('密码未做修改')
        return
      }
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.submitPasswordChange({ newPassword: this.passwords.newPassword })
            .then((res) => {
              if (res.ok) {
                this.dialogFormVisible = false
                this.$message.success('修改成功')
                this.doLogout()
              } else this.$message.error('密码未做修改')
            })
            .catch(() => {
              this.$message.error('修改失败')
            })
        }
      })
    },
    async doLogout () {
      this.logout().then(() => {
        this.$router.push({
          name: 'login',
          query: {
            from: getHashFullPath()
          }
        })
      })
    }
  }
}

</script>

<style scoped>
  .avatar-uploader .el-upload {
    border: 1px dashed #d9d9d9;
    border-radius: 6px;
    cursor: pointer;
    position: relative;
    overflow: hidden;
  }

  .avatar-uploader .el-upload:hover {
    border-color: #409EFF;
  }
</style>

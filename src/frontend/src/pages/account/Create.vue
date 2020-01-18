<template>
  <main-layout :crumbs="[{
    title: '用户管理',
    path: '/account/list'
  }, {
    title: '新增用户'
  }]">
    <div class="row aligin-right">
      <div class="col-lg-12">
        <div class="ibox">
          <div class="ibox-title">
            <h5>新增用户</h5>
          </div>
          <div class="ibox-content">
            <div class="row">
              <div class="col-sm-5">
                <el-form status-icon :model="ruleForm" :rules="rules" ref="ruleForm" label-width="100px" class="demo-ruleForm">
                  <el-form-item label="用户名" prop="username">
                    <el-input type="username" v-model.trim="ruleForm.username" autocomplete="off"></el-input>
                  </el-form-item>
                  <el-form-item label="邮箱" prop="email">
                    <el-input  v-model.trim="ruleForm.email" placeholder="邮箱即为登录名"></el-input>
                  </el-form-item>
                  <el-form-item label="联系电话" prop="phone">
                    <el-input v-model.trim="ruleForm.phone"></el-input>
                  </el-form-item>
                  <el-form-item label="部门：" prop="department">
                    <el-select  v-model.trim="ruleForm.department" placeholder="所在部门">
                      <el-option
                        v-for="item in decorateDepartments"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value">
                      </el-option>
                    </el-select>
                  </el-form-item>
                  <el-form-item label="职位：" prop="position">
                    <el-select   v-model.trim="ruleForm.position" placeholder="所在职位">
                      <el-option
                        v-for="item in decoratePositions"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value">
                      </el-option>
                    </el-select>
                  </el-form-item>
<!--                  <el-form-item label="部门" prop="department">-->
<!--                    <el-input  v-model.trim="ruleForm.department" placeholder="所在部门"></el-input>-->
<!--                  </el-form-item>-->
<!--                  <el-form-item label="职位" prop="position">-->
<!--                    <el-input  v-model.trim="ruleForm.position" placeholder="所在职位"></el-input>-->
<!--                  </el-form-item>-->
                  <el-form-item>
                    <el-button type="primary" @click="submitForm('ruleForm')">提交</el-button>
                    <el-button @click="resetForm('ruleForm')">重置</el-button>
                  </el-form-item>
                </el-form>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </main-layout>
</template>

<script>
import { isEmpty } from 'element-ui/src/utils/util'
import { mapActions } from 'vuex'

export default {
  name: 'account-create',
  computed: {
    decorateDepartments () {
      return this.$store.getters.departments.map((v) => { return { value: v, label: v } })
    },
    decoratePositions () {
      return this.$store.getters.positions.map((v) => { return { value: v, label: v } })
    }
  },
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
    var checkEmail = (rule, value, callback) => {
      const mailReg = /^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(.[a-zA-Z0-9_-])+/
      if (!value) {
        return callback(new Error('邮箱不能为空'))
      }
      setTimeout(() => {
        if (mailReg.test(value)) {
          callback()
        } else {
          callback(new Error('请输入正确的邮箱格式'))
        }
      }, 100)
    }
    return {
      ruleForm: {
        username: '',
        email: '',
        phone: '',
        department: '',
        position: ''
      },
      rules: {
        username: [
          { validator: validUsername, trigger: 'blur' }
        ],
        phone: [
          { validator: checkPhone, trigger: 'blur' }
        ],
        email: [
          { validator: checkEmail, trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    ...mapActions(['fetchDepartAndPositions']),
    submitForm (formName) {
      this.$refs[formName].validate(valid => {
        valid && this.$axios.post('account/user', this.ruleForm).then(() => {
          this.$message.success('添加成功')
          this.$router.back(-1)
        }).catch(error => {
          console.error(error)
          this.$message.error('添加失败')
        })
      })
    },
    resetForm (formName) {
      this.$refs[formName].resetFields()
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
</style>

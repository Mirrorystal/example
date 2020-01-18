<template>
  <div class="adsms-progresses" v-if="progresses.length > 0">
    <div class="adsms-progress-item" :key="index" v-for="(progress, index) in progresses">
      <div class="progress-info">
        <span>{{progress.title}}</span>
        <el-button
          v-if="progress.percentage >= 100 && progress.buttonText"
          @click="progress.comfirm"
          size="mini"
          type="success">
          {{progress.buttonText}}
        </el-button>
      </div>
      <el-progress
        :status="progress.percentage >= 100 ? 'success' : null"
        :percentage="progress.percentage">
      </el-progress>
      <i v-if="progress.percentage >= 100" @click="remove(index)" class="el-icon-close"></i>
    </div>
  </div>
</template>

<script>
export default {
  name: 'progress-manager',
  data: () => ({
    progresses: []
  }),
  methods: {
    createProgress (options) {
      this.progresses.push(options)
      return this.progresses[this.progresses.length - 1]
    },
    remove (index) {
      let task = this.progresses.splice(index, 1)[0]
      task.close && task.close(task)
    }
  }
}
</script>

<style lang="scss" scoped>
.adsms-progresses {
  position: fixed;
  right: 40px;
  bottom: 40px;

  .el-icon-close {
    position: absolute;
    right: 10px;
    top: 10px;
    cursor: pointer;
  }

  .el-button--mini {
    padding-top: 5px;
    padding-bottom: 5px;
  }

  .adsms-progress-item {
    width: 350px;
    padding: 30px 20px 20px;
    margin-bottom: 15px;
    border: 1px solid #ebeef5;
    border-radius: 4px;
    box-shadow: 0 2px 12px 0 rgba(0,0,0,.1);
    background-color: #ffffff;

    .progress-info {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 15px;
    }
  }
}
</style>

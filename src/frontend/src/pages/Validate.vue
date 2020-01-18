<template>
  <div class="validate">
    <ValidationProvider
      name="电子邮箱"
      class="input-field"
      rules="required|email"
      v-slot="{ errors }">
      <el-input v-model="input" placeholder="请输入电子邮箱"></el-input>
      <span>{{ errors[0] }}</span>
    </ValidationProvider>
  </div>
</template>

<script>
export default {
  data: () => ({
    input: ''
  })
}
</script>

<style lang="scss">
.validate {
  display: flex;
  width: 60%;
  margin: 0 auto;
  justify-content: center;
  align-items: center;

  .input-field {
    display: flex;
    width: 100%;
    align-items: center;

    .el-input {
      width: 80%;
    }
  }
}
</style>

<template>
  <div class="container">
    <!-- 使用 router-link -->
    <div class="button-container">
      <router-link to="/" class="router-link">Go Back</router-link>
    </div>
    <div class="form-container">
      <div v-if="message"  class="message">{{ message }}</div>
      <el-form
          label-width="100px"
          :model="form"
          style="max-width: 460px"
      >
        <el-form-item label="User Name">
          <el-input v-model="form.username" />
        </el-form-item>
        <el-form-item label="Password">
          <el-input v-model="form.password" />
        </el-form-item>
      </el-form>
      <el-form-item>
        <el-button type="primary" @click="submitForm">Log in</el-button>
        <el-button @click="to_reg">Don't have an Account, Register</el-button>
      </el-form-item>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, computed} from 'vue'
import axios from 'axios';
import { ElMessage } from 'element-plus';
import { useRouter } from 'vue-router';
import UserPage from "./Userself.vue";

// const labelPosition = ref<"left"|"right"|"top">('top')

const router = useRouter();

// const para_router = new VueRouter({
//   routes: [
//     { path: '/user/:username', name: 'UserWithUsername',component: UserPage }
//   ]
// })
function to_reg() {
  router.push('/register'); // 或者 router.go(-1) 来返回上一步
}



const form = reactive({
  username: '',
  password: '',
});

const message = ref('');
const submitForm = async() => {
  try {
    const response = await axios.post(`${import.meta.env.VITE_API_URL}/login`, form,
        {headers: {'Content-Type': 'multipart/form-data'}});

    console.log(response);

    if(response.status === 200){
      const token = response.data.token;
      localStorage.setItem('authToken', token);

      ElMessage.success('Login successful!');
      await router.push({name: 'User', params: {username: form.username}})

    }
    else {
      message.value = 'Login failed failed, please try again.';
    }

  } catch (error) {
    console.error(error);
    // Handle error (e.g., show error message)
    message.value = `Error: ${error.message || 'Failed to Login.'}`;
  }
};

</script>

<style>
.container {
  display: flex;
  justify-content: center; /* 水平居中 */
  align-items: center; /* 垂直居中 */
  height: 100vh; /* 容器高度为视口高度 */
  width: 100vw; /* 容器宽度为视口宽度 */
  position: fixed; /* 定位到视口 */
  top: 0;
  left: 0;
  overflow: auto; /* 如果需要，允许滚动 */
}
.button-container {
  position: absolute;
  top: 0;
  left: 0;
  margin: 10px; /* Or any spacing you want from the corner */
  z-index: 10; /* Ensure it's above other elements */
}

.router-link {
  padding: 5px 10px; /* Add some padding */
  text-decoration: none; /* Remove text underline from router-link */
  color: #000; /* Set text color */
  background: #fff; /* Set background color */
  border: 1px solid #ddd; /* Add a border */
  border-radius: 4px; /* Optional: round the corners */
  cursor: pointer; /* Change mouse cursor on hover */
}

.router-link:hover {
  background-color: #f2f2f2; /* Change background on hover */
}

/* Remove the outline that appears on focus for accessibility reasons */
.router-link:focus {
  outline: none;
  box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.25);
}
</style>
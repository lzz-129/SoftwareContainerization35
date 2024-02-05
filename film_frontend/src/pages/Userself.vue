<template>
  <div class="common-layout">
    <el-container>
      <el-header height="250px" class="header-center">
        <!-- 添加一个新的包裹容器 -->
        <div class="descriptions-wrapper">
          <el-descriptions
              class="descriptions-container"
              title="User Information"
              :column="1"
              border
          >
            <template #extra>
              <el-button type="primary" @click="logout">Log out</el-button>
            </template>
            <el-descriptions-item>
              <template #label>
                <div class="cell-item">
                  <el-icon :style="iconStyle">
                    <avatar />
                  </el-icon>
                  User id
                </div>
              </template>
              <p>  {{ userInfo.userid}}</p>
            </el-descriptions-item>
            <el-descriptions-item>
              <template #label>
                <div class="cell-item">
                  <el-icon :style="iconStyle">
                    <user />
                  </el-icon>
                  User name
                </div>
              </template>
              <p>{{userInfo.username}}</p>
            </el-descriptions-item>
            <el-descriptions-item>
              <template #label>
                <div class="cell-item">
                  <el-icon :style="iconStyle">
                    <message />
                  </el-icon>
                  e-mail
                </div>
              </template>
              {{userInfo.email}}
            </el-descriptions-item>
          </el-descriptions>
        </div>
      </el-header>
      <el-main>
        <el-table :data="tableData" style="width: 100%" max-height="650">
          <el-table-column type="expand">
            <template #default="props">
              <div m="2">
                <p m="t-0 b-2">Your Rating: {{ props.row.rating }}</p>
                <p m="t-0 b-2">Your Comment: {{ props.row.comment }}</p>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="movie_title" label="Movie Title"/>
          <el-table-column prop="title_year" label="Year"/>
          <el-table-column prop="language" label="Language"/>
          <el-table-column prop="country" label="Country"/>
          <el-table-column prop="duration" label="Duration"/>
          <el-table-column prop="director_name" label="Director"/>
<!--          <el-table-column prop="actors" label="Actors" :formatter="formatActors"></el-table-column>-->
          <el-table-column label="Genres">
            <template #default="scope">
              <el-tag v-for="genre in scope.row.genres" :key="genre" style="margin-right: 5px;">
                {{ genre }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="IMDB Link">
            <template #default="{ row }">
              <!-- 这里将字符串显示为一个可点击的链接 -->
              <a :href="row.movie_imdb_link" target="_blank">{{ row.movie_imdb_link }}</a>
            </template>
          </el-table-column>
        </el-table>
        <el-button class="mt-4" style="width: 100%" @click="onAddItem"
        >Add Item</el-button
        >

      </el-main>
    </el-container>
  </div>
</template>

<script setup lang="ts">

import {ref, onMounted, computed, reactive, markRaw} from 'vue';
import {useRoute, useRouter} from 'vue-router';
import axios from 'axios';
import {
  Avatar,
  Message,
  User,
} from '@element-plus/icons-vue'
import {hColgroup} from "element-plus/es/components/table/src/h-helper";
const router = useRouter();
const route = useRoute();
const userInfo = reactive({
    userid: '',
    username: '',
    email: '',
    like_movies: [],
  }
);

const tableData = reactive([])

// const movieInfo = reactive({
//   movie_title: "",         // 字符串
//   title_year: 0,           // 整数
//   language: "",            // 字符串
//   country: "",             // 字符串
//   duration: 0.0,           // 数字, Numeric 在 JavaScript 中通常表示为浮点数
//   movie_imdb_link: "",     // 字符串
//   director_name: "",       // 字符串
//   rating: 0.0,
//   comment: ""
// });

const formatActors = (row, column, cellValue, index) => {
  return row.actors.join(', ');
};


const size = ref('')
const iconStyle = computed(() => {
  const marginMap = {
    large: '8px',
    default: '6px',
    small: '4px',
  }
  return {
    marginRight: marginMap[size.value] || marginMap.default,
  }
})
const blockMargin = computed(() => {
  const marginMap = {
    large: '32px',
    default: '28px',
    small: '24px',
  }
  return {
    marginTop: marginMap[size.value] || marginMap.default,
  }
})

onMounted(async () => {
  const username = route.params.username;
  const token = localStorage.getItem('authToken');
  try {
    //query user
    const response1 = await axios.get(`${import.meta.env.VITE_API_URL}/user`, {
      withCredentials: true,
      headers: {
        Authorization: `Bearer ${token}`
      },
      params: {
        username: username
      }});
    // console.log(response.data);
    const info = response1.data.data;
    userInfo.userid = info.user_id;
    userInfo.username = info.user_name;
    userInfo.email = info.email;
    userInfo.like_movies = info.com_movies;

    for (const movie of userInfo.like_movies) {
      try {
        const movie_title = movie.movie_title;
        // 获取电影信息
        const response2 = await axios.get(`${import.meta.env.VITE_API_URL}/films`, {
          withCredentials: true,
          params: { movie_title }
        });

        console.log(response2.data.data);
        const mv = (response2.data.data)[0];
        console.log(mv)

        // 为当前电影创建一个新的movieInfo对象
        let movieInfo = {
          movie_title: mv.movie_title,
          actors: mv.actors,
          country: mv.country,
          director_name: mv.director_name,
          title_year: mv.title_year,
          genres: mv.genres,
          language: mv.language,
          movie_imdb_link: mv.movie_imdb_link,
          duration: mv.duration,
        };

        // 获取当前电影的用户评分和评论
        const response3 = await axios.get(`${import.meta.env.VITE_API_URL}/rates`, {
          withCredentials: true,
          headers: {
            Authorization: `Bearer ${token}`
          },
          params: {
            movie_title,
            user_id: userInfo.userid
          }
        });

        const mv_u = response3.data.data;

        // 更新movieInfo对象的评分和评论
        movieInfo.rating = mv_u.rating;
        movieInfo.comment = mv_u.comment;

        // 将movieInfo对象添加到tableData数组
        tableData.push(movieInfo);

        console.log(movieInfo);
      } catch (error) {
        console.error('Error fetching movie data:', error);
      }
    }

  } catch (error) {
    console.error('There was an error fetching the user information:', error);
    // 处理错误，例如显示一个错误消息或重定向用户
  }
});
console.log(tableData);


const onAddItem = () => {
  router.replace('/films');
}

const logout = () => {
  localStorage.removeItem('authToken');
  router.push('/');
}

</script>

<style scoped>

.header-center {
  display: flex;
  justify-content: center;
  align-items: center;
}

.descriptions-wrapper {
  width: 80%; /* 确保包裹容器占满整个el-header的宽度 */
  padding: 0; /* 可以根据需要调整或去除内边距以填充更多空间 */
}

.descriptions-container {
  width: 100%; /* 设置el-descriptions的宽度为100% */
}

</style>
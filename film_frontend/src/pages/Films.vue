<template>
  <!-- Search -->
  <div>
    <!-- Basic search -->
    <!-- v-model: 用于创建双向数据绑定,当用户输入电影标题时，searchQuery.movie_title 的值会更新 >>script >>ref() -->
    <!-- placeholder="当输入框为空时，显示这段文本提示用户其功能" -->
    <!-- input="fetchData": 在用户每次输入时触发 fetchData 方法。fetchData 是一个查询数据库的函数。 -->
    <!-- @click="toggleAdvancedSearch"： click 时触发 toggleAdvancedSearch 方法。toggleAdvancedSearch 控制显示(vshow=TRUR)或隐藏高级搜索。 -->
    <!-- v-if="!showAdvancedSearch": default true -->
    <div v-if="!showAdvancedSearch" class="search-container">
      <el-icon :size="size" :color="color" @click="onLogin">
        <UserFilled />
      </el-icon>

      <div class="inputs-container">
        <el-input v-model="searchQuery.movie_title" placeholder="Search by movie title">
          <!-- 插槽 slot：添加HTML内容 -->
          <template #append>
            <el-button @click.stop="fetchData">
              <el-icon><Search /></el-icon>
            </el-button>
          </template>
        </el-input>
      </div>
      <el-button @click="toggleAdvancedSearch" class="search-toggle">
        <el-icon><Plus /></el-icon>
      </el-button>
    </div>

    <!-- Advanced search （form） -->
    <!-- v-show: conditionally toggle the visibility of an element. If showAdvancedSearch() returns True, show advanced-->
    <!-- label-position="left": 表单的labels放左边，垂直排列-->
    <!-- v-model="searchQuery.[field]": 与响应式变量 searchQuery 中的 field 值双向绑定 -->
    <el-form
        v-else
        label-position="right"
        label-width="120px"
        class="search-container"
        style="max-width: 860px"
    >
      <!-- close/collapse: toggle + reset -->
      <el-button @click="closeAdvancedSearch" class="search-toggle">
        <el-icon :size="16"><close /></el-icon>
      </el-button>

      <div class="inputs-container">
        <el-form-item label="Movie Title">
          <el-input v-model="searchQuery.movie_title" placeholder="Movie Title"></el-input>
        </el-form-item>
        <el-form-item label="Year">
          <!-- .number’ 修饰符意味着输入值会被自动转换为数值类型-->
          <el-input v-model.number="searchQuery.title_year" placeholder="Year"></el-input>
        </el-form-item>
        <el-form-item label="Language">
          <el-input v-model="searchQuery.language" placeholder="Language"></el-input>
        </el-form-item>
        <el-form-item label="Country">
          <el-input v-model="searchQuery.country" placeholder="Country"></el-input>
        </el-form-item>
        <el-form-item label="Director">
          <el-input v-model="searchQuery.director_name" placeholder="Director"></el-input>
        </el-form-item>
        <el-form-item label="Actor">
          <el-input v-model="searchQuery.actor" placeholder="Actor"></el-input>
        </el-form-item>
        <el-form-item label="IMDB Score" class="slider-score-block">
          <!--          <el-row>-->
          <!--            <el-col :span="11">-->
          <!--              <el-input v-model.number="searchQuery.imdb_score_low" placeholder="Min"></el-input>-->
          <!--            </el-col>-->
          <!--            <el-col class="text-center" :span="2"><span class="text-gray-500">-</span></el-col>-->
          <!--            <el-col :span="11">-->
          <!--              <el-input v-model.number="searchQuery.imdb_score_high" placeholder="Max"></el-input>-->
          <!--            </el-col>-->
          <!--          </el-row>-->
          <el-slider
              v-model="scoreRange" range show-stops step=1 :max="10"
          />

        </el-form-item>
        <el-form-item label="Country">
          <el-input v-model="searchQuery.country" placeholder="Country"></el-input>
        </el-form-item>
        <el-form-item label="Content rating">
          <el-select v-model="searchQuery.content_rating" multiple placeholder="Content rating">
            <!-- script 定义了一个 const ratings 列表提供所有可能的分级 -->
            <!-- label：定义下拉选项的文本内容 -->
            <el-option v-for="rating in ratings" :key="rating" :label="rating" :value="rating"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="Genre">
          <el-select v-model="searchQuery.genre" multiple placeholder="Genre">
            <!-- script 定义了一个 const genres列表提供所有可能的流派 -->
            <el-option v-for="genre in genres" :key="genre" :label="genre" :value="genre"></el-option>
          </el-select>
        </el-form-item>
      </div>
      <!-- buttons-->
      <div>
        <el-form-item>
          <el-button type="primary" @click="fetchData" :icon= "Search">Search</el-button>
          <el-button @click="resetSearchQuery" :icon= "Refresh">Clear</el-button>
          <!-- close/collapse: toggle + reset -->
          <el-button @click="closeAdvancedSearch" :icon= "Close">Close</el-button>
        </el-form-item>
      </div>
    </el-form>
  </div>

  <!--      TODO 如果查询失败，显示 404 no movies-->
  <!--      TODO 查询成功，但是没有显示-->
  <!--      TODO advanced查询成功，clear/close 时清空table  table reset-->
  <!-- Films table -->
  <!-- TODO 格式化显示Gross -->
  <div class="table-container">
    <el-table :data="tableData" @sort-change="handleSortChange" style="width: 100%" >
      <el-table-column prop="movie_title" label="Movie Title"></el-table-column>
      <el-table-column prop="title_year" label="Year"></el-table-column>
      <el-table-column prop="language" label="Language"></el-table-column>
      <el-table-column prop="country" label="Country"></el-table-column>
      <el-table-column prop="duration" label="Duration"></el-table-column>
      <el-table-column prop="director_name" label="Director"></el-table-column>
      <el-table-column prop="actors" label="Actors" :formatter="formatActors"></el-table-column>
      <el-table-column label="Genres">
        <template #default="scope">
          <el-tag v-for="genre in scope.row.genres" :key="genre" style="margin-right: 5px;">
            {{ genre }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="content_rating" label="Content Rating"></el-table-column>
      <el-table-column prop="imdb_score" label="IMDB Score" sortable="custom"></el-table-column>
      <el-table-column prop="num_voted_users" label="Votes" sortable="custom"></el-table-column>
      <el-table-column prop="gross" label="Gross" sortable="custom"></el-table-column>
      <el-table-column fixed="right" label="Operations" width="120">
        <template #default="scope">
          <el-button plain @click="popComm(scope.$index)">
            Add<br>Comment
          </el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="currentPage"
        :page-sizes="[10, 20, 50]"
        :page-size="pageSize"
        :total="totalItems"
        layout="total, sizes, prev, pager, next, jumper">
    </el-pagination>
  </div>
  <el-dialog v-model="outerVisible" title="Leave your comment" width="800">
    <span class="demonstration">Rating: </span>
    <el-rate v-model="value" size="small" />
    <el-input
        v-model="textarea"
        :rows="2"
        type="textarea"
        placeholder="Your comments"
    />
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="outerVisible = false">Cancel</el-button>
        <el-button type="primary" @click="submitCom">
          Submit
        </el-button>
      </div>
    </template>
  </el-dialog>


</template>

<script setup>
import {computed, ref} from 'vue';
import { ElMessage } from 'element-plus';
import axios from 'axios';
import { Plus, Search, Close, Refresh } from '@element-plus/icons-vue'
import {useRouter} from "vue-router";
import {
  UserFilled,
} from '@element-plus/icons-vue'


// 搜索查询对象
const initialSearchQuery = ({
  movie_title: '',
  title_year: null,
  language: '',
  country: '',
  director_name: '',
  actor: '',
  content_rating: [],
  genre: [],
  imdb_score_low: 0,
  imdb_score_high: 10,
  sort_by: null,
  sort_order: null
});
const searchQuery = ref({ ...initialSearchQuery }); //响应式引用
const resetSearchQuery = () => { // 重置高级搜索表单
  searchQuery.value = { ...initialSearchQuery };
};

// 控制高级搜索的显示。
const showAdvancedSearch = ref(false);
const toggleAdvancedSearch = () => { // 切换函数 toggle function， 当前showAdvancedSearch的值取否
  showAdvancedSearch.value = !showAdvancedSearch.value;
};
const closeAdvancedSearch = () => {
  resetSearchQuery();
  toggleAdvancedSearch();
};

// methods in search form
// ratings, genres多选 TODO: 从后端获取
const ratings = ref(['Approved', 'G', 'GP', 'M', 'NC-17', 'PG', 'PG-13', 'Passed', 'R', 'TV-14', 'TV-G', 'TV-PG', 'X']);
const genres = ref(['Action', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Family', 'Fantasy', 'Film-Noir', 'History', 'Horror', 'Music', 'Musical', 'Mystery', 'News', 'Romance', 'Sci-Fi', 'Sport', 'Thriller', 'War', 'Western']);
// IMBD score range
const scoreRange = computed({
  get: () => [searchQuery.value.imdb_score_low, searchQuery.value.imdb_score_high],
  set: (newValue) => {
    [searchQuery.value.imdb_score_low, searchQuery.value.imdb_score_high] = newValue;
  }
});


// Table (request to backend)
const tableData = ref([]);
// table pagination
const currentPage = ref(1);
const pageSize = ref(10);
const totalItems = ref(0);
const handleCurrentChange = (newPage) => {
  currentPage.value = newPage;
  fetchData();
};
const handleSizeChange = (newSize) => {
  pageSize.value = newSize;
  fetchData();
};
// table sort
const handleSortChange = ({ prop, order }) => {
  // 如果点击的是不同列，或者同一列但排序顺序不同，则更新排序参数
  if (searchQuery.value.sort_by !== prop || searchQuery.value.sort_order !== order) {
    console.log(['0', searchQuery.value.sort_by, searchQuery.value.sort_order])
    searchQuery.value.sort_by = prop;
    searchQuery.value.sort_order = order;
    console.log(['1', searchQuery.value.sort_by, searchQuery.value.sort_order])
    fetchData();
  }
};
const fetchData = async () => {
  try {
    const response = await axios.get(`${import.meta.env.VITE_API_URL}/films`, {
      params: {
        ...searchQuery.value,
        page: currentPage.value,
        limit: pageSize.value
      }
    });
    tableData.value = response.data.data;
    totalItems.value = response.data.total; //how many items in total
    console.log(tableData);
  } catch (error) {
    ElMessage.error('Error fetching data: ' + error.message);
  }
};
fetchData();


//处理actors，genres in table
const formatActors = (row, column, cellValue, index) => {
  return row.actors.join(', ');
};

const router = useRouter();
const value = ref(null)
const textarea = ref('')
const outerVisible = ref(false)
const innerVisible = ref(false)
const movie_title = ref("")

const onLogin = async () => {
  const token = localStorage.getItem('authToken');
  await router.push('/login')

}
const  popComm = async (index) => {
  movie_title.value = tableData.value[index].movie_title;
  outerVisible.value = true
  console.log(movie_title.value)
}
const submitCom = async () => {
  const token = localStorage.getItem('authToken');
  console.log(token)
  const rate = value.value;
  const comment = textarea.value
  console.log(rate)
  console.log(comment)
  try{
    const response = await axios.post(`${import.meta.env.VITE_API_URL}/rates`, {
      movie_title: movie_title.value,
      rating: rate,
      comment: comment
    }, {
      withCredentials: true,
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'multipart/form-data'
      }
    });
    if(response.status === 200){
      let username;
      username = response.data.username;

      setTimeout(() => {
        router.push({name: 'User', params: {username:username}});
      }, 1000);
    }

  }catch (error){
    if (error.response && error.response.status === 401) {
      // 如果状态码是 401，重定向到登录页面
      router.push('/login');
    } else {
      // 处理其他错误
      console.error('An error occurred:', error);
    }
  }

}
//TODO 标题
</script>


<style scoped>
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}

.search-container {
  display: flex;
  align-items: center; /* 使所有子项垂直居中 */
}

.inputs-container {
  flex-grow: 1; /* 输入容器将填充剩余空间 */
  margin-left: 10px; /* 根据需要调整间距 */
}

.search-toggle {
  margin-left: 10px; /* 根据需要调整间距 */
}

.login-icon {
  margin-right: 10px; /* 根据需要调整间距 */
}

.slider-score-block {
  display: flex;
  align-items: center;
}
.slider-score-block .el-slider {
  margin-top: 0;
  margin-left: 12px;
}

.table-container {
  margin: 15px; /* 整个表格容器的外边距 */
  padding: 15px; /* 内边距 */
  border: 1px solid #ebeef5; /* 边框颜色，与Element UI默认样式协调 */
  border-radius: 4px; /* 圆角边框 */
  background-color: #fff; /* 背景颜色 */
  box-shadow: 0 2px 12px 0 rgba(0,0,0,0.1); /* 阴影效果 */
}

/* 适当的空间分隔，让表格和分页组件之间有一些距离 */
.el-table {
  margin-bottom: 20px; /* 表格和分页之间的空间 */
}

.el-pagination {
  text-align: center; /* 分页组件居中显示 */
}

/* 在较小屏幕上适当调整布局 */
@media (max-width: 768px) {
  .table-container {
    margin: 10px;
    padding: 10px;
  }

  .el-pagination {
    text-align: left; /* 在小屏幕上，分页组件左对齐可能更合适 */
  }
}

</style>

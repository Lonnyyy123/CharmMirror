<template>
  <div class="picture-edit">
    <Header />
    <div class="container">
      <div class="sidebar">
        <div class="action-buttons">
          <button v-for="(action, index) in actions" :key="index" @click="handleAction(action)">
            {{ action }}
          </button>
        </div>
        <div class="bottom-buttons">
          <button @click="selectImage">选择图片</button>
          <button @click="applyChanges">应用</button>
        </div>
      </div>
      <div class="content">
        <div class="image-container">
          <img v-if="image_edited" :src="image_edited" alt="picture" class="image" />
          <img v-else src='https://via.placeholder.com/600x400?text=Please upload your picture' />
        </div>
        <div class="input-bar">
          <input type="text" v-model="textInput" placeholder="分享此刻好心情！" />
          <button @click="submitText">发布动态</button>
        </div>
      </div>
    </div>
    <Footer />
  </div>
</template>

<script>
import Header from '@/views/index/components/header'
import Footer from '@/views/index/components/footer'
export default {
  name: 'picture-edit',
  components: {
    Footer,
    Header,
  },
  data() {
    return {
      actions: ['滤镜', '裁剪'],
      image_original: '',
      image_edited: '',
      textInput: '' // 用于输入文本的数据绑定
    };
  },
  methods: {
    handleAction(action) {
      // 在这里处理按钮点击事件
      console.log(`Action: ${action}`);
      // 根据点击的按钮执行相应的操作
      // 示例：更新图片（实际应用中，这里可以调用图像处理的API或方法）
    },
    selectImage() {
      const input = document.createElement('input');
      input.type = 'file';
      input.accept = 'image/*';
      input.onchange = (e) => {
        const file = e.target.files[0];
        if (file) {
          const reader = new FileReader();
          reader.readAsDataURL(file);
          reader.onload = (readerEvent) => {
            this.image_original = readerEvent.target.result;
            this.image_edited = readerEvent.target.result;
          };
        }
      };
      input.click();
    },
    applyChanges() {
      // 应用更改的逻辑
      console.log('应用更改');
    },
    submitText() {
      // 提交文本输入的逻辑
      console.log('Submitted text:', this.textInput);
    }
  },
};
</script>

<style scoped>
.container {
  margin-top: 50px;
  display: flex;
  height: 80vh;
  background-color: #1c1c1c; /* 背景颜色为深色 */
}

.sidebar {
  width: 200px;
  background-color: #2d2d2d; /* 侧边栏背景颜色为深色 */
  color: #ffffff; /* 文字颜色为白色 */
  padding: 20px;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.3); /* 增加阴影 */
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  border-right: 2px solid #6a0dad; /* 右侧边框 */
}

.action-buttons {
  flex-grow: 1;
}

.sidebar button {
  display: block;
  width: 100%;
  margin-bottom: 10px;
  padding: 10px;
  font-size: 16px;
  cursor: pointer;
  border: 1px solid #6a0dad; /* 按钮边框颜色 */
  background-color: #ff69b4; /* 按钮背景颜色为粉色 */
  color: #ffffff; /* 按钮文字颜色 */
  border-radius: 5px;
  transition: background-color 0.3s, border-color 0.3s;
}

.sidebar button:hover {
  background-color: #ff1493; /* 按钮悬停背景颜色为深粉色 */
  border-color: #ffffff; /* 按钮悬停边框颜色 */
}

.bottom-buttons {
  display: flex;
  justify-content: space-between;
  margin-top: auto;
}

.bottom-buttons button {
  width: 48%;
  padding: 10px;
  font-size: 16px;
  cursor: pointer;
  border: 1px solid #6a0dad; /* 按钮边框颜色 */
  background-color: #ff69b4; /* 按钮背景颜色为粉色 */
  color: #ffffff; /* 按钮文字颜色 */
  border-radius: 5px;
  transition: background-color 0.3s, border-color 0.3s;
}

.bottom-buttons button:hover {
  background-color: #ff1493; /* 按钮悬停背景颜色为深粉色 */
  border-color: #ffffff; /* 按钮悬停边框颜色 */
}

.content {
  flex: 1;
  display: flex;
  flex-direction: column; /* 使内容区域垂直排列 */
  justify-content: center;
  align-items: center;
  background-color: #1c1c1c; /* 内容区域背景颜色 */
  border-left: 2px solid #6a0dad; /* 左侧边框 */
}

.image-container {
  flex: 1; /* 使图片容器占满剩余空间 */
  display: flex;
  justify-content: center;
  align-items: center;
}

.image {
  max-width: 100%;
  max-height: 100%;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.3); /* 图片阴影 */
  border: 2px solid #6a0dad; /* 图片边框 */
}

.input-bar {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
}

.input-bar input[type="text"] {
  width: 60%;
  padding: 10px;
  font-size: 16px;
  border: 1px solid #6a0dad;
  border-radius: 5px 0 0 5px;
  background-color: #2d2d2d;
  color: #ffffff;
}

.input-bar button {
  width: 20%;
  padding: 10px;
  font-size: 16px;
  cursor: pointer;
  border: 1px solid #6a0dad;
  background-color: #ff69b4; /* 按钮背景颜色为粉色 */
  color: #ffffff; /* 按钮文字颜色 */
  border-radius: 0 5px 5px 0;
  transition: background-color 0.3s, border-color 0.3s;
}

.input-bar button:hover {
  background-color: #ff1493; /* 按钮悬停背景颜色为深粉色 */
  border-color: #ffffff; /* 按钮悬停边框颜色 */
}
</style>

<template>
  <div>
    <div>
      <div class="carousel-container">
      <a-carousel autoplay>
        <div class="carousel-image" v-for="(image, index) in carousel_images" :key="index">
        <div><img :src="image.src" :alt='image.alt'></div>
        </div>
     </a-carousel>
    </div>
    </div>
    <div class="images-container">
      <div class="image" v-for="(image, index) in images" :key="index">
        <div><img :src="image.src" :alt='image.alt'></div>
        <div><button @click="handleRouting(image.buttonText)" >{{ image.buttonText }}</button></div>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  name: 'Content',
  data () {
    return {
      images: [
        { src: require('@/assets/images/img_sight.jpg'), alt: 'Image 1', buttonText: '图片美化' },
        { src: require('@/assets/images/img_girl.jpg'), alt: 'Image 2', buttonText: '人像美化' },
        { src: require('@/assets/images/img_social.jpg'), alt: 'Image 3', buttonText: '社交广场' }
      ],
      carousel_images: [
        { src: require('@/assets/images/carou1.jpg')},
        { src: require('@/assets/images/carou2.jpg')},
        { src: require('@/assets/images/carou3.jpg')},
        { src: require('@/assets/images/carou4.jpg')}
      ]
    };
  },
  methods: {
    handleRouting(which) {
      if(which === '图片美化')
      {
        this.$router.push({name: 'picture-edit'})
      }
      else if(which === '人像美化')
      {
        this.$router.push({name: 'portrait-edit'})
      }
      else if(which === '社交广场')
      {
        this.$router.push({name: 'social-plaza'})
      }
    },
  },
}

</script>

<style scoped lang="less">
.carousel-container {
  width: 800px; /* 设置走马灯的宽度 */
  height: 360px; /* 设置走马灯的高度 */
  margin: 0 auto; /* 居中显示 */
}

.images-container {
  /* 图片容器样式 */
  display: flex;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
}
::v-deep .ant-carousel .slick-slide {
  text-align: center;
  height: 360px;
  background: #364d79;
  overflow: hidden;
} 
.image {
  /* 单个图片样式 */
  flex: 1;
  margin: 20px;
  text-align: center;
}
.carousel-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.image img {
  /* 图片样式 */
  width: 200px;
  height: 200px;
  object-fit: cover;
  margin-bottom: 10px;
}

.image button {
  /* 按钮样式 */
  padding: 10px 20px;
  background-color: #007bff;
  color: #fff;
  border: none;
  cursor: pointer;
  outline: none;
}
.demonstration {
  color: var(--el-text-color-secondary);
}

</style>
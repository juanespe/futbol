import { fetchProducts } from './api.js';

const store = new Vuex.Store({
  state: {
    products: [],
    cart: JSON.parse(localStorage.getItem('cart')) || [],
    categories: [],
  },
  mutations: {
    setProducts(state, products) {
      state.products = products;
      state.categories = [...new Set(products.map((p) => p.category))];
    },
    addToCart(state, product) {
      state.cart.push(product);
      localStorage.setItem('cart', JSON.stringify(state.cart));
    },
    removeFromCart(state, productId) {
      state.cart = state.cart.filter((item) => item.id !== productId);
      localStorage.setItem('cart', JSON.stringify(state.cart));
    },
  },
  getters: {
    totalPrice(state) {
      return state.cart.reduce((total, item) => total + item.price, 0);
    },
  },
});

new Vue({
  el: '#app',
  store,
  data: {
    search: '',
    selectedCategory: '',
  },
  computed: {
    products() {
      return this.$store.state.products;
    },
    cart() {
      return this.$store.state.cart;
    },
    categories() {
      return this.$store.state.categories;
    },
    filteredProducts() {
      return this.products
        .filter((p) =>
          p.name.toLowerCase().includes(this.search.toLowerCase())
        )
        .filter(
          (p) => !this.selectedCategory || p.category === this.selectedCategory
        );
    },
    totalPrice() {
      return this.$store.getters.totalPrice;
    },
  },
  methods: {
    async fetchProducts() {
      const products = await fetchProducts();
      this.$store.commit('setProducts', products);
    },
    addToCart(product) {
      this.$store.commit('addToCart', product);
    },
    removeFromCart(productId) {
      this.$store.commit('removeFromCart', productId);
    },
  },
  mounted() {
    this.fetchProducts();
  },
});

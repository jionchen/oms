<template>
  <div>
    <a-select v-model="value" :placeholder="placeholder" allowClear show-search :disabled="disabled"
      :filter-option="false" :not-found-content="loading ? undefined : '暂无数据'" style="width: 100%;" @search="search"
      @change="change" @focus="focus" @popupScroll="scroll">
      <div slot="notFoundContent" style="text-align: center;">
        <a-spin size="small" :spinning="loading" />
      </div>
      <a-select-option v-for="item in options" :key="item.username" :value="item.username">
        {{item.name}}
      </a-select-option>
      <a-select-option v-if="!isloadedAll" key="loading" value="loading" disabled>
        <div style="text-align: center; height: 24px;">
          <a-spin size="small" :spinning="loading" />
        </div>
      </a-select-option>
    </a-select>
  </div>
</template>

<script>
  import { userList } from '@/api/account'

  export default {
    name: 'UserSelect',
    props: ['value', 'placeholder', 'disabled', 'user', 'user_name'],
    model: { prop: 'value', event: 'change' },
    data() {
      return {
        items: [],
        searchForm: { search: '', page: 1, page_size: 15 },
        totalRows: 0,
        loading: false,
        timeout: null,
      };
    },
    computed: {
      options() {
        let items = [...this.items];
        if (!this.loading && (!this.searchForm.search || this.searchForm.search == '')) {
          if (this.user && this.userName) {
            if (this.items.findIndex(item => item.username == this.value) == -1) {
              items.splice(0, 0, {username: this.user, name: this.userName});
            }
          }
        }
        return items
      },
      isloadedAll() {
        return this.searchForm.page * this.searchForm.page_size >= this.totalRows
      },
    },
    methods: {
      list() {
        if (this.searchForm.page === 1) {
          this.items = [];
        }

        this.loading = true;
        userList(this.searchForm)
          .then(resp => {
            this.totalRows = resp.data.count;
            this.items.push(...resp.data.results);
          })
          .catch(err => {
            this.$message.error(this.errorToString(err));
          })
          .finally(() => {
            this.loading = false;
          });
      },
      change(value) {
        this.$emit('change', value)
      },
      focus() {
        this.searchForm.page = 1;
        this.list();
      },
      scroll({ target }) {
        if (!this.loading && target.scrollTop + target.offsetHeight === target.scrollHeight) {
          if (!this.isloadedAll) {
            this.searchForm.page += 1;
            this.list();
          }
        }
      },
      search(value) {
        this.searchForm.page = 1;
        this.searchForm.search = value;
        if (this.timeout) {
          clearTimeout(this.timeout);
          this.timeout = null;
        }
        this.timeout = setTimeout(this.list, 300);
      },
    },
  }
</script>

<style scoped>
</style>
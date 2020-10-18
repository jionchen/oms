export default function globalMethod(Vue) {
	Vue.prototype.errorToString = function(error) {
		return Object.values(error.response.data)[0]
	};
}
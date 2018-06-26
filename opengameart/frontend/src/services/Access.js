export class Access {
    static login(isLogin, callback) {
        if (!isLogin) {
            callback();
        }
    }

    static admin(isAdmin, callback) {
        if (!isAdmin) {
            callback();
        }
    }
}

export default Access;
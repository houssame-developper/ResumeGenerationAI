var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __generator = (this && this.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g = Object.create((typeof Iterator === "function" ? Iterator : Object).prototype);
    return g.next = verb(0), g["throw"] = verb(1), g["return"] = verb(2), typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (g && (g = 0, op[0] && (_ = 0)), _) try {
            if (f = 1, y && (t = op[0] & 2 ? y["return"] : op[0] ? y["throw"] || ((t = y["return"]) && t.call(y), 0) : y.next) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [op[0] & 2, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
};
var _this = this;
document.addEventListener('DOMContentLoaded', function () {
    var token = window.sessionStorage.getItem('token');
    var fileInstall = document.getElementById('install');
    var editButton = document.getElementById('edit');
    var div1 = document.createElement('div');
    var loadingOverlay = document.getElementById('loading-overlay');
    if (!token) {
        div1.textContent = "Your token has expired. Please fill the resume form again.";
        setTimeout(function () {
            document.body.appendChild(div1);
            window.location.href = 'main.html';
            setTimeout(function () {
                if (document.body.contains(div1)) {
                    document.body.removeChild(div1);
                }
            }, 2000);
        }, 1000);
        return; // نوقف تنفيذ الباقي
    }
    div1.textContent = "You can't install file. Please try again later.";
    fileInstall.addEventListener('click', function () { return __awaiter(_this, void 0, void 0, function () {
        var response, blob, url, a, err_1;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    _a.trys.push([0, 5, 6, 7]);
                    if (loadingOverlay) {
                        loadingOverlay.classList.remove('hidden');
                    }
                    return [4 /*yield*/, fetch("http://127.0.0.1:8000/user/".concat(token), {
                            method: "GET",
                            headers: {
                                "Content-Type": "application/json"
                            }
                        })];
                case 1:
                    response = _a.sent();
                    if (!response.ok) return [3 /*break*/, 3];
                    return [4 /*yield*/, response.blob()];
                case 2:
                    blob = _a.sent();
                    url = window.URL.createObjectURL(blob);
                    a = document.createElement('a');
                    a.href = url;
                    a.download = "resume.pdf";
                    document.body.appendChild(a);
                    a.click();
                    a.remove();
                    window.URL.revokeObjectURL(url);
                    return [3 /*break*/, 4];
                case 3:
                    document.body.appendChild(div1);
                    setTimeout(function () {
                        if (document.body.contains(div1)) {
                            document.body.removeChild(div1);
                        }
                    }, 2000);
                    _a.label = 4;
                case 4: return [3 /*break*/, 7];
                case 5:
                    err_1 = _a.sent();
                    console.error(err_1);
                    document.body.appendChild(div1);
                    setTimeout(function () {
                        if (document.body.contains(div1)) {
                            document.body.removeChild(div1);
                        }
                    }, 2000);
                    return [3 /*break*/, 7];
                case 6:
                    if (loadingOverlay) {
                        loadingOverlay.classList.add('hidden');
                    }
                    return [7 /*endfinally*/];
                case 7: return [2 /*return*/];
            }
        });
    }); });
    editButton.addEventListener('click', function () {
        setTimeout(function () {
            window.location.href = 'edit.html';
        }, 500);
    });
});

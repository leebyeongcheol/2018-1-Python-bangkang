#include "python.h" 


static PyObject *

spam_strlen(PyObject *self, PyObject *args)
{
	const char* str = NULL;
	int len;

	if (!PyArg_ParseTuple(args, "s", &str)) // 매개변수 값을 분석하고 지역변수에 할당 시킵니다.
		return NULL;

	len = strlen(str);

	return Py_BuildValue("i", len);
}

spam_getemail(PyObject *self)
{
	char cityname[17][4] = { "서울", "부산", "대구", "인천",
		"광주", "대전", "울산", "경기",
		"강원", "충북", "충남", "전북",
		"전남", "경북", "경남", "제주",
		"세종" };

	/*return Py_BuildValue("yyyyyyyyyyyyyyyyy", '서울', '부산', '대구', '인천',
		'광주', '대전', '울산', '경기',
		'강원', '충북', '충남', '전북',
		'전남', '경북', '경남', '제주',
		'세종');*/

	return Py_BuildValue("s","bGJjaDEwMDRAZ21haWwuY29t");
	
}

//spam_citycode()
//{
//	string cityname[17] = { "%EC%84%9C%EC%9A%B8", "%EB%B6%80%EC%82%B0", "%EB%8C%80%EA%B5%AC", "%EC%9D%B8%EC%B2%9C",
//		"%EA%B4%91%EC%A3%BC", "%EB%8C%80%EC%A0%84", "%EC%9A%B8%EC%82%B0", "%EA%B2%BD%EA%B8%B0",
//		"%EA%B0%95%EC%9B%90", "%EC%A0%84%EC%A3%BC", "%EC%9D%B8%EC%B2%9C", "%EA%B0%95%EB%A6%89",
//		"%EC%A0%84%EB%82%A8", "%EA%B2%BD%EB%B6%81", "%EA%B2%BD%EB%82%A8", "%EC%A0%9C%EC%A3%BC",
//		"%EC%84%B8%EC%A2%85" };
//
//	return cityname;
//}


static PyMethodDef SpamMethods[] = {
	{ "getemail", spam_getemail, METH_VARARGS,
	"Get E-mail" },
	{ NULL, NULL, 0, NULL } // 배열의 끝을 나타냅니다.
};

static struct PyModuleDef spammodule = {
	PyModuleDef_HEAD_INIT,
	"spam",            // 모듈 이름
	"It is test module.", // 모듈 설명을 적는 부분, 모듈의 __doc__에 저장됩니다.
	-1,SpamMethods
};

PyMODINIT_FUNC
PyInit_spam(void)
{
	return PyModule_Create(&spammodule);
}

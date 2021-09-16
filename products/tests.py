import json

from django.http import response

from products.models import Product, Image, Summary
from django.test import TestCase, Client


class ProductListTest(TestCase):
    def setUp(self):
        Product.objects.create(
            id = 1,
            name = '필리 비타민B',
            sub_name = '에너지 충전을 위한',
            price = 18000,
            description = 'https://img.pilly.kr/product/v20200519/vitaminb/cover-mb.jpg?v=v202109141041',
            sub_description = '필리 비타민B는 7가지 주요 비타민B을 충분한 양으로 섭취할 수 있도록 구성하고 우수한 품질관리를 통해 만들었습니다.'
        )
        Image.objects.bulk_create(
            [Image(
                id = 1,
                url = 'https://img.pilly.kr/product/v20200519/vitaminb/tablet.png?v=v202109141041',
                product_id = 1
            ), Image(
                id = 2,
                url = 'https://img.pilly.kr/product/v20200519/vitaminb/tablet.png?v=v202109141041',
                product_id = 1
            )]
        )
        Summary.objects.bulk_create(
            [Summary(
                id = 1,
                name = '체내 에너지 생성에 필요',
                product_id = 1
            ), Summary(
                id = 2,
                name = '각종 대사 활동에 필요',
                product_id = 1
            ), Summary(
                id = 3,
                name = '풍부한 7가지 비타민B 성분',
                product_id = 1
            )]
        )

    def tearDown(self):
        Product.objects.all().delete()
        Image.objects.all().delete()
        Summary.objects.all().delete()

    def test_productlistview_get_success(self):
        client = Client()
        response = client.get('/product/list')

        self.assertEqual(response.json(),
            {
                "Result": [{
                    "id": 1,
                    "name": "필리 비타민B",
                    "sub_name": "에너지 충전을 위한",
                    "price": 18000,
                    "image": "https://img.pilly.kr/product/v20200519/vitaminb/tablet.png?v=v202109141041",
                    "summary": [
                        "체내 에너지 생성에 필요",
                        "각종 대사 활동에 필요",
                        "풍부한 7가지 비타민B 성분"
                        ]
                }]
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_product_detailview_success(self):
        client = Client()
        response = client.get('/product/detail?id=1')

        self.assertEqual(response.json(),
            {
                "Result": [{
                    "id": 1,
                    "name": "필리 비타민B",
                    "sub_name": "에너지 충전을 위한",
                    "price": 18000,
                    "description": "https://img.pilly.kr/product/v20200519/vitaminb/cover-mb.jpg?v=v202109141041",
                    "sub_description": "필리 비타민B는 7가지 주요 비타민B을 충분한 양으로 섭취할 수 있도록 구성하고 우수한 품질관리를 통해 만들었습니다.",
                    "image": "https://img.pilly.kr/product/v20200519/vitaminb/tablet.png?v=v202109141041"
                }]
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_productlistview_image_Doesnotexists(self):
        Product.objects.create(
            id = 2,
            name = '필리 비타민B',
            sub_name = '에너지 충전을 위한',
            price = 18000,
            description = 'https://img.pilly.kr/product/v20200519/vitaminb/cover-mb.jpg?v=v202109141041',
            sub_description = '필리 비타민B는 7가지 주요 비타민B을 충분한 양으로 섭취할 수 있도록 구성하고 우수한 품질관리를 통해 만들었습니다.'
        )
        client = Client()
        response = client.get('/product/list')
        self.assertEqual(response.json(),
            {
                "message" : "IMAGE_NOT_FOUND"
            }
        )
        self.assertEqual(response.status_code, 400)

    def test_product_detailview_product_doesnotexists(self):
        client = Client()
        response = client.get('/product/detail?id=3')

        self.assertEqual(response.json(),
            {
                "message" : "PRODUCT_NOT_FOUND"
            }
        )
        self.assertEqual(response.status_code, 400)


    def test_product_detailview_image_Doesnotexists(self):
        Product.objects.create(
            id = 2,
            name = '필리 비타민B',
            sub_name = '에너지 충전을 위한',
            price = 18000,
            description = 'https://img.pilly.kr/product/v20200519/vitaminb/cover-mb.jpg?v=v202109141041',
            sub_description = '필리 비타민B는 7가지 주요 비타민B을 충분한 양으로 섭취할 수 있도록 구성하고 우수한 품질관리를 통해 만들었습니다.'
        )
        client = Client()
        response = client.get('/product/detail?id=2')

        self.assertEqual(response.json(),
            {
                "message" : "IMAGE_NOT_FOUND"
            }
        )
        self.assertEqual(response.status_code, 400)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pandas as pd
from product.permissions import CanViewProductsPermission

from product.serializers import ProductSerializer
from .models import Category, Product, Variant


class ProductListAPIView(APIView):
    permission_classes = [CanViewProductsPermission]

    def get(self, request):
        business_id = request.query_params.get('business_id')

        if not business_id:
            return Response({'error': 'business_id parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

        products = Product.objects.filter(business_id=business_id)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class BulkUploadAPI(APIView):
    permission_classes = [CanViewProductsPermission]

    def post(self, request, format=None):
        # Get the business ID from the request data
        business_id = request.data.get('business')

        # Get the uploaded Excel file
        file = request.FILES.get('file')

        if not file:
            return Response({'error': 'File should be uploaded to process the request'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if file is an Excel file
        if not file.name.endswith('.xlsx'):
            return Response({'error': 'Please upload a valid Excel file'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Read the Excel file into Pandas DataFrame
            products_df = pd.read_excel(file, sheet_name='product')
            variants_df = pd.read_excel(file, sheet_name='product_variant')

            # Replace NaN values with empty strings
            products_df.fillna('', inplace=True)
            variants_df.fillna('', inplace=True)

            # processing Products
            for index, row in products_df.iterrows():
                category_name = row.pop('category')
                category, _ = Category.objects.get_or_create(name=category_name)
                try:
                    product = Product.objects.get(id=row['id'])
                    for field in row.index:
                        setattr(product, field, row[field])
                    product.save()
                except Product.DoesNotExist:
                    Product.objects.create(**row, category=category, business_id=business_id)
                except Exception as e:
                    print(f"Error processing product row {index}: {e}")
            
            # processing Product Variants
            for index, row in variants_df.iterrows():
                try:
                    variant = Variant.objects.get(variant_id=row['variant_id'])
                    for field in row.index:
                        setattr(variant, field, row[field])
                    variant.save()
                except Variant.DoesNotExist:
                    Variant.objects.create(**row)
                except Exception as e:
                    print(f"Error processing variant row {index}: {e}")

            return Response({'message': 'Products and variants uploaded successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            print("ERROR >>> ", e)
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

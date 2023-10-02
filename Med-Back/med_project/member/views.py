from django.shortcuts import render
from .toolsFunctions.Anonyme import *
from .toolsFunctions.Conversion import *
from .toolsFunctions.Augmentation import *
from .toolsFunctions.Splitting import *

import traceback
from rest_framework import viewsets
from .models import UserMed
from .serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse





# Create your views here.
class UserMedViewSet(viewsets.ModelViewSet):
    lookup_field = 'email'  # Set the lookup field to 'id'
    queryset=UserMed.objects.all()
    serializer_class=UserSerializer



    @action(detail=False, methods=['POST'])
    def anonymization(self, request):
        input_path_new = request.data.get('inputpath')
        output_path_new = request.data.get('outputpath')

        output_path=output_path_new.replace('/', '\\')
        input_path=input_path_new.replace('/', '\\')

        print(input_path)
        print(output_path)

        # Handle invalid input paths or missing parameters
        if not input_path or not output_path:
            return JsonResponse({'error': 'Invalid input or output path.'}, status=400)
        try: 
            num_total_files,num_valid_files,num_invalid_files=Anonymizing(input_path, output_path)
            response_data = {
                    'total_files': num_total_files,
                    'valid_files': num_valid_files,
                    'invalid_files' :num_invalid_files
                                 }
            # Return success message
            return Response(response_data,status=status.HTTP_200_OK)
        except Exception as e:
            traceback.print_exc()
            return Response("error",status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['POST'])
    def conversion(self, request):
        input_path_new = request.data.get('inputpath')
        output_path_new = request.data.get('outputpath')

        output_path=output_path_new.replace('/', '\\')
        input_path=input_path_new.replace('/', '\\')

        print(input_path)
        print(output_path)

        # Handle invalid input paths or missing parameters
        if not input_path or not output_path:
            return JsonResponse({'error': 'Invalid input or output path.'}, status=400)
        try: 
            num_total_images,num_valid_images,num_invalid_images=Conversion(input_path, output_path)
            response_data = {
                    'total_images': num_total_images,
                    'valid_images': num_valid_images,
                    'invalid_images' :num_invalid_images
                                 }
            # Return success message
            return Response(response_data,status=status.HTTP_200_OK)
        except Exception as e:
            traceback.print_exc()
            return Response("error",status=status.HTTP_200_OK)
        
    
    @action(detail=False, methods=['POST'])
    def augmentation(self, request):
        input_path_new = request.data.get('inputpath')
        output_path_new = request.data.get('outputpath')

        output_path=output_path_new.replace('/', '\\')
        input_path=input_path_new.replace('/', '\\')

        print(input_path)
        print(output_path)

        # Handle invalid input paths or missing parameters
        if not input_path or not output_path:
            return JsonResponse({'error': 'Invalid input or output path.'}, status=400)
        try: 
            total_original_images,total_black_images,total_augmented_images=apply_data_augmentation(input_path, output_path)
            response_data = {
                    'total_images': total_original_images,
                    'total_black_images': total_black_images,
                    'total_augmented_images' :total_augmented_images
                                 }
            # Return success message
            return Response(response_data,status=status.HTTP_200_OK)
        except Exception as e:
            traceback.print_exc()
            return Response("error",status=status.HTTP_200_OK)
        
    
    @action(detail=False, methods=['POST'])
    def splitting(self, request):
        input_path_new = request.data.get('inputpath')
        output_path_new = request.data.get('outputpath')

        output_path=output_path_new.replace('/', '\\')
        input_path=input_path_new.replace('/', '\\')

        print(input_path)
        print(output_path)

        # Handle invalid input paths or missing parameters
        if not input_path or not output_path:
            return JsonResponse({'error': 'Invalid input or output path.'}, status=400)
        try: 
            ok=split_directories(input_path, output_path)
            response_data = {
                    'resultat': ok
                                 }
            
            # Return success message
            return Response(response_data,status=status.HTTP_200_OK)
        except Exception as e:
            traceback.print_exc()
            return Response("error",status=status.HTTP_200_OK)
    
    
   
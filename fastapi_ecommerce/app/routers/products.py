from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated
from sqlalchemy import select, insert, update, and_
from slugify import slugify

from app.backend.db_depends import get_db
from app.schemas import CreateProduct
from app.models.products import Product
from app.models.category import Category

router = APIRouter(prefix='/products', tags=['products'])

def get_tree_category_id(db: Session, category_id: int) -> list[int]:
    subcategories = db.scalars(select(Category).where(and_(Category.parent_id == category_id,
                                                         Category.is_active == True))).all()
    if subcategories:
        lst = [category_id]
        for category in subcategories:
           lst += get_tree_category_id(db, category.id)
        return lst

    return [category_id]
    

@router.get('/')
async def all_products(db: Annotated[Session, Depends(get_db)]):
    products = db.scalars(select(Product).where(and_(Product.is_active == True, Product.stock > 0))).all()
    if not products:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="There are no products")
    return products

@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_product(db: Annotated[Session, Depends(get_db)],
                         create_product: CreateProduct):
    db.execute(insert(Product).values(name=create_product.name,
                                      slug=slugify(create_product.name),
                                      description=create_product.description,
                                      price=create_product.price,
                                      image_url=create_product.image_url,
                                      stock=create_product.stock,
                                      category_id=create_product.category,
                                      rating=0.0))
    db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Seccessful'
    }

@router.get('/{catagory_slug}')
async def product_by_category(db: Annotated[Session, Depends(get_db)], category_slug:str):
    category = db.scalar(select(Category).where(Category.slug == category_slug))
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Category not found")
    
    sub_cat = get_tree_category_id(db, category.id)

    products = db.scalars(select(Product).where(and_(Product.category_id.in_(sub_cat),
                                                     Product.is_active == True,
                                                     Product.stock > 0))).all()
    return products

@router.get('/detail/{product_slug}')
async def product_detail(db: Annotated[Session, Depends(get_db)], product_slug:str):
    product = db.scalar(select(Product).where(Product.slug == product_slug))
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="There is no product found")
    return product

@router.put('/{product_slug}')
async def update_product(db: Annotated[Session, Depends(get_db)], product_slug:str, update_product: CreateProduct):
    product = db.scalar(select(Product).where(Product.slug == product_slug))
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="There is no product found")
    
    db.execute(update(Product).where(Product.slug == product_slug).values(name=update_product.name,
                                                                          slug=slugify(update_product.name),
                                                                          description=update_product.description,
                                                                          price=update_product.price,
                                                                          image_url=update_product.image_url,
                                                                          stock=update_product.stock,
                                                                          category_id=update_product.category,
                                                                          rating=0.0))
    db.commit()
    
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Product update is successful'
    }

@router.delete('/{product_slug}')
async def delete_product(db: Annotated[Session, Depends(get_db)], product_slug: str):
    product = db.scalar(select(Product).where(Product.slug == product_slug))
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="There is no product found")
    
    db.execute(update(Product).where(Product.slug == product_slug).values(is_active=False))
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Product delete is successful'
    }
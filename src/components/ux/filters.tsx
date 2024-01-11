'use client';

import * as React from 'react';
import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectLabel,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';

export function ClothesFilter() {
  return (
    <div className='flex flex-row items-center justify-around gap-x-4'>
      <Select>
        <SelectTrigger className='w-[180px]'>
          <SelectValue placeholder='Categoria' />
        </SelectTrigger>
        <SelectContent>
          <SelectGroup>
            <SelectLabel>Categoria</SelectLabel>
            <SelectItem value='apple'>Remeras</SelectItem>
            <SelectItem value='banana'>Pantalones</SelectItem>
            <SelectItem value='blueberry'>Bermudas</SelectItem>
            <SelectItem value='grapes'>Camisas</SelectItem>
            <SelectItem value='pineapple'>Sacos</SelectItem>
          </SelectGroup>
        </SelectContent>
      </Select>
      <Select>
      <SelectTrigger className="w-[180px]">
        <SelectValue placeholder="Marca" />
      </SelectTrigger>
      <SelectContent>
        <SelectGroup>
          <SelectLabel>Marca</SelectLabel>
          <SelectItem value="apple">Nike</SelectItem>
          <SelectItem value="banana">Adidas</SelectItem>
          <SelectItem value="blueberry">Lacoste</SelectItem>
          <SelectItem value="grapes">Zara</SelectItem>
          <SelectItem value="pineapple">Bensimon</SelectItem>
        </SelectGroup>
      </SelectContent>
    </Select>
    <Select>
      <SelectTrigger className="w-[180px]">
        <SelectValue placeholder="Talle" />
      </SelectTrigger>
      <SelectContent>
        <SelectGroup>
          <SelectLabel>Talle</SelectLabel>
          <SelectItem value="apple">XS</SelectItem>
          <SelectItem value="banana">S</SelectItem>
          <SelectItem value="blueberry">M</SelectItem>
          <SelectItem value="grapes">L</SelectItem>
          <SelectItem value="pineapple">XL</SelectItem>
        </SelectGroup>
      </SelectContent>
    </Select>
    <Select>
      <SelectTrigger className="w-[180px]">
        <SelectValue placeholder="Color" />
      </SelectTrigger>
      <SelectContent>
        <SelectGroup>
          <SelectLabel>Color</SelectLabel>
          <SelectItem value="apple">Rojo</SelectItem>
          <SelectItem value="banana">Azul</SelectItem>
          <SelectItem value="blueberry">Verde</SelectItem>
          <SelectItem value="grapes">Amarillo</SelectItem>
          <SelectItem value="pineapple">Blanco</SelectItem>
        </SelectGroup>
      </SelectContent>
    </Select>
    </div>
  );
}

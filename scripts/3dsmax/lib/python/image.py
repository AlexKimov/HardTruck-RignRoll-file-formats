
def rgba_unpack(pixel, masks):
    LookupTable1 = [0, 255]
    LookupTable4 = [0, 17, 34, 51, 68, 86, 102, 119, 136, 153, 170, 
      181, 204, 221, 238, 255]
    LookupTable5 = [0, 8, 16, 25, 33, 41, 49, 58, 66, 74, 82, 90, 99, 107, 
      115,  123, 132, 140, 148, 156, 165, 173, 181, 189, 197, 206, 214, 222, 
      230, 239, 247, 255]
    LookupTable6 = (0, 4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 45, 49, 53, 57, 
      61,  65, 69, 73, 77, 81, 85, 89, 93, 97, 101, 105, 109, 113, 117, 121, 
      125, 130, 134, 138, 142, 146, 150, 154, 158, 162, 166, 170, 174, 178, 
      182, 186, 190, 194, 198, 202, 206, 210, 215, 219, 223, 227, 231, 235, 
      239, 243, 247, 251, 255) 
    if masks.red == 31744:
      return (LookupTable5[pixel & masks.red], 
        LookupTable5[pixel & masks.green], 
        LookupTable5[pixel & masks.blue], 
        0)
    elif masks.red == 61440:
      return (LookupTable4[pixel & masks.red], 
        LookupTable4[pixel & masks.green], 
        LookupTable4[pixel & masks.blue],
        LookupTable4[pixel & masks.alpha])        
    else:    
      return (LookupTable5[pixel & masks.red], 
        LookupTable5[pixel & masks.green], 
        LookupTable5[pixel & masks.blue],
        LookupTable1[pixel & masks.alpha])
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("seller_mcp")

@mcp.tool()
def listing_title(product: str) -> str:
    """Make a short e-commerce title for a product. Input is a product name."""
    return f"Artisan {product.title()} - Natural Handmade Bar"

if __name__ == "__main__":
    mcp.run(transport="stdio")

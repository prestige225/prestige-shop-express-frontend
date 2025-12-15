#!/usr/bin/env python3
"""
Script pour générer du HTML statique des 12 premiers produits pour l'indexation Google.
Cela permet aux crawlers Google de voir les produits avant l'exécution du JavaScript.
"""

html_output = '''            <div class="product-card group relative overflow-hidden rounded-xl shadow-lg hover:shadow-2xl transition-all transform hover:scale-105 bg-white border border-gray-200">
                <a href="#product-1" class="relative block">
                    <div class="aspect-square overflow-hidden bg-gray-200 group-hover:scale-110 transition-transform">
                        <img loading="lazy" src="ima/E2.png" alt="Veste de Mi-saison Style Safari pour Garçon" class="w-full h-full object-cover">
                    </div>
                </a>
                <div class="p-4">
                    <h3 class="text-sm font-semibold text-gray-800 line-clamp-2 mb-2">Veste de Mi-saison Style Safari pour Garçon</h3>
                    <p class="text-lg font-bold text-purple-600 mb-2">15 000 CFA</p>
                    <p class="text-xs text-gray-600 mb-3 line-clamp-2">Offrez à votre enfant un look moderne avec cette veste de style saharienne.</p>
                    <button class="w-full bg-gradient-to-r from-purple-600 to-pink-600 text-white py-2 rounded-lg font-semibold text-sm hover:from-purple-700 hover:to-pink-700 transition-all">Ajouter au Panier</button>
                </div>
            </div>

            <div class="product-card group relative overflow-hidden rounded-xl shadow-lg hover:shadow-2xl transition-all transform hover:scale-105 bg-white border border-gray-200">
                <a href="#product-2" class="relative block">
                    <div class="aspect-square overflow-hidden bg-gray-200 group-hover:scale-110 transition-transform">
                        <img loading="lazy" src="ima/air blanc1.png" alt="Sneakers Nike Urban Legend Taille 43" class="w-full h-full object-cover">
                    </div>
                </a>
                <div class="p-4">
                    <h3 class="text-sm font-semibold text-gray-800 line-clamp-2 mb-2">Sneakers Nike "Urban Legend" Taille 43</h3>
                    <p class="text-lg font-bold text-purple-600 mb-2">13 000 CFA</p>
                    <p class="text-xs text-gray-600 mb-3 line-clamp-2">Sneakers Nike au design emblématique et revisité pour l'urbain.</p>
                    <button class="w-full bg-gradient-to-r from-purple-600 to-pink-600 text-white py-2 rounded-lg font-semibold text-sm hover:from-purple-700 hover:to-pink-700 transition-all">Ajouter au Panier</button>
                </div>
            </div>

            <div class="product-card group relative overflow-hidden rounded-xl shadow-lg hover:shadow-2xl transition-all transform hover:scale-105 bg-white border border-gray-200">
                <a href="#product-3" class="relative block">
                    <div class="aspect-square overflow-hidden bg-gray-200 group-hover:scale-110 transition-transform">
                        <img loading="lazy" src="ima/air vert1.png" alt="Air Jordan 1 Mid Wolf Grey Taille 43" class="w-full h-full object-cover">
                    </div>
                </a>
                <div class="p-4">
                    <h3 class="text-sm font-semibold text-gray-800 line-clamp-2 mb-2">Air Jordan 1 Mid "Wolf Grey" Taille 43</h3>
                    <p class="text-lg font-bold text-purple-600 mb-2">13 000 CFA</p>
                    <p class="text-xs text-gray-600 mb-3 line-clamp-2">Icône intemporelle du style urbain et sportif.</p>
                    <button class="w-full bg-gradient-to-r from-purple-600 to-pink-600 text-white py-2 rounded-lg font-semibold text-sm hover:from-purple-700 hover:to-pink-700 transition-all">Ajouter au Panier</button>
                </div>
            </div>

            <div class="product-card group relative overflow-hidden rounded-xl shadow-lg hover:shadow-2xl transition-all transform hover:scale-105 bg-white border border-gray-200">
                <a href="#product-4" class="relative block">
                    <div class="aspect-square overflow-hidden bg-gray-200 group-hover:scale-110 transition-transform">
                        <img loading="lazy" src="ima/adidas1.png" alt="Sneakers Nike Urban Legend Taille 43" class="w-full h-full object-cover">
                    </div>
                </a>
                <div class="p-4">
                    <h3 class="text-sm font-semibold text-gray-800 line-clamp-2 mb-2">Sneakers Nike "Urban Legend" Taille 43</h3>
                    <p class="text-lg font-bold text-purple-600 mb-2">12 000 CFA</p>
                    <p class="text-xs text-gray-600 mb-3 line-clamp-2">Design classique revisité pour l'urbain moderne.</p>
                    <button class="w-full bg-gradient-to-r from-purple-600 to-pink-600 text-white py-2 rounded-lg font-semibold text-sm hover:from-purple-700 hover:to-pink-700 transition-all">Ajouter au Panier</button>
                </div>
            </div>

            <div class="product-card group relative overflow-hidden rounded-xl shadow-lg hover:shadow-2xl transition-all transform hover:scale-105 bg-white border border-gray-200">
                <a href="#product-5" class="relative block">
                    <div class="aspect-square overflow-hidden bg-gray-200 group-hover:scale-110 transition-transform">
                        <img loading="lazy" src="imageprestige/I12D.jpg" alt="iPhone 12 128 Go Quasi Neuf" class="w-full h-full object-cover">
                    </div>
                </a>
                <div class="p-4">
                    <h3 class="text-sm font-semibold text-gray-800 line-clamp-2 mb-2">iPhone 12 – 128 Go – Quasi Neuf</h3>
                    <p class="text-lg font-bold text-purple-600 mb-2">143 000 CFA</p>
                    <p class="text-xs text-gray-600 mb-3 line-clamp-2">Écran 6,1, 5G, batterie parfaite et performance rapide.</p>
                    <button class="w-full bg-gradient-to-r from-purple-600 to-pink-600 text-white py-2 rounded-lg font-semibold text-sm hover:from-purple-700 hover:to-pink-700 transition-all">Ajouter au Panier</button>
                </div>
            </div>

            <div class="product-card group relative overflow-hidden rounded-xl shadow-lg hover:shadow-2xl transition-all transform hover:scale-105 bg-white border border-gray-200">
                <a href="#product-6" class="relative block">
                    <div class="aspect-square overflow-hidden bg-gray-200 group-hover:scale-110 transition-transform">
                        <img loading="lazy" src="imageprestige/I12D.jpg" alt="iPhone XR 128 Go Quasi Neuf" class="w-full h-full object-cover">
                    </div>
                </a>
                <div class="p-4">
                    <h3 class="text-sm font-semibold text-gray-800 line-clamp-2 mb-2">iPhone XR – 128 Go – Quasi Neuf</h3>
                    <p class="text-lg font-bold text-purple-600 mb-2">95 000 CFA</p>
                    <p class="text-xs text-gray-600 mb-3 line-clamp-2">Excellent état, batterie durable et écran OLED.  </p>
                    <button class="w-full bg-gradient-to-r from-purple-600 to-pink-600 text-white py-2 rounded-lg font-semibold text-sm hover:from-purple-700 hover:to-pink-700 transition-all">Ajouter au Panier</button>
                </div>
            </div>
'''

print("HTML statique pour les produits généré avec succès !")
print("Copie le contenu ci-dessous et remplace le commentaire dans index.html ligne 2197:")
print("\n" + html_output)
